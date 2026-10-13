"""Measure public SDK calls separately from decoding, without SDK internals.

Run from submission/: uv run python ../tests/audit_performance.py --help
"""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import resource
import sys
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "submission"))

from src import __main__ as application
from src.decoder import (
    Decoder, MODEL_DIRECTORY, load_decoder, vocabulary_bytes,
)
import run_evaluation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=("public", "private", "changed", "probes"),
                        default="public")
    parser.add_argument("--device", choices=("auto", "cpu"), default="auto")
    parser.add_argument("--limit", type=int, help="Measure only the first N batch prompts")
    parser.add_argument("--output", type=Path, required=True,
                        help="New directory for metrics and results")
    args = parser.parse_args()
    if args.limit is not None and (args.limit < 1 or args.suite == "probes"):
        parser.error("--limit requires a positive size and a batch suite")
    args.output.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parent
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in Path("src").glob("*.py")}
    started = time.monotonic()
    if args.device == "cpu":
        MODEL_DIRECTORY.mkdir(parents=True, exist_ok=True)
        os.environ["HF_HUB_CACHE"] = str(MODEL_DIRECTORY.resolve())
        from llm_sdk import Small_LLM_Model

        model = Small_LLM_Model(device="cpu", trust_remote_code=False)
        decoder = Decoder(model=model, vocabulary=vocabulary_bytes(
            Path(model.get_path_to_vocab_file()),
        ))
    else:
        decoder = load_decoder()
    load_seconds = time.monotonic() - started
    sdk_type = type(decoder.model)
    original_logits = sdk_type.get_logits_from_input_ids
    original_call = Decoder.call
    original_inputs = application.load_inputs
    records = []
    current = {}

    def limited_inputs(*paths):
        functions, prompts = original_inputs(*paths)
        return functions, prompts[:args.limit]

    def measured_logits(model, ids):
        begin = time.monotonic()
        try:
            return original_logits(model, ids)
        finally:
            stats = current.setdefault("values", {
                "calls": 0, "seconds": 0.0, "context_tokens": 0,
            })
            stats["calls"] += 1
            stats["seconds"] += time.monotonic() - begin
            stats["context_tokens"] += len(ids)

    def measured_call(self, prompt, functions):
        nonlocal current
        current = {"prompt": prompt}
        begin = time.monotonic()
        try:
            return original_call(self, prompt, functions)
        finally:
            current["seconds"] = time.monotonic() - begin
            records.append(current)

    output = args.output / "results.json"
    if args.suite == "probes":
        argv = ["run_evaluation.py", "0", "17", str(output)]
        entrypoint = run_evaluation.main
    else:
        argv = ["src", "--output", str(output)]
        if args.suite == "private":
            inputs = root / "moulinette/private/input"
            argv += ["--functions_definition", str(inputs / "functions_definition.json"),
                     "--input", str(inputs / "function_calling_tests.json")]
        elif args.suite == "changed":
            argv += ["--functions_definition", str(root / "changed_functions.json"),
                     "--input", str(root / "changed_prompts.json")]
        entrypoint = application.main
    begin = time.monotonic()
    with patch.object(sdk_type, "get_logits_from_input_ids", measured_logits), \
            patch.object(Decoder, "call", measured_call), \
            patch("src.decoder.load_decoder", return_value=decoder), \
            patch.object(application, "load_inputs", limited_inputs), \
            patch.object(run_evaluation, "load_decoder", return_value=decoder), \
            patch.object(sys, "argv", argv):
        status = entrypoint()
    elapsed = time.monotonic() - begin
    metrics = {
        "platform": platform.platform(), "python": platform.python_version(),
        "device": str(decoder.model.encode("device").device),
        "threads": {key: os.environ.get(key) for key in
                    ("OMP_NUM_THREADS", "MKL_NUM_THREADS")},
        "suite": args.suite, "reasoning_mode": "disabled",
        "prompt_limit": args.limit,
        "source_sha256": hashes,
        "versions": {name: importlib.metadata.version(name) for name in
                     ("numpy", "pydantic", "torch", "transformers")},
        "peak_process_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        * (1 if sys.platform == "darwin" else 1024),
        "model_load_seconds": load_seconds, "batch_seconds": elapsed,
        "total_seconds": load_seconds + elapsed, "exit_status": status,
        "prompts": records,
    }
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(f"Audit: load {load_seconds:.1f}s; batch {elapsed:.1f}s; "
          f"total {load_seconds + elapsed:.1f}s", flush=True)
    return status


if __name__ == "__main__":
    sys.exit(main())
