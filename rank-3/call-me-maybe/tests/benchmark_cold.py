"""Time the ordinary CLI with a fresh model cache in an isolated submission.

Run from submission/: uv run python ../tests/benchmark_cold.py --output DIR
DIR must be new. Dependency setup is recorded separately; inference timing
includes uv/Python startup, model downloads, loading and writing the results.
Existing model files and environments are never removed or reused by the copy.
"""

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--suite", choices=("public", "private", "changed"),
                        default="public")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    tests = Path(__file__).resolve().parent
    source = tests.parent / "submission"
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "."], cwd=source,
    ).decode().split("\0")
    tracked = [name for name in tracked if name]
    hashes = {name: hashlib.sha256((source / name).read_bytes()).hexdigest()
              for name in tracked}
    with tempfile.TemporaryDirectory(prefix="fresh-", dir=output) as temporary:
        workspace = Path(temporary) / "submission"
        for name in tracked:
            destination = workspace / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, destination)
        environment = dict(os.environ)
        for key in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "VIRTUAL_ENV",
                    "UV_PROJECT_ENVIRONMENT", "PYTHONPATH",
                    "TRANSFORMERS_CACHE", "PYTORCH_TRANSFORMERS_CACHE",
                    "PYTORCH_PRETRAINED_BERT_CACHE"):
            environment.pop(key, None)
        environment.update({
            "HF_HOME": str(Path(temporary) / "huggingface"),
            "HF_HUB_CACHE": str(workspace / "model"),
            "HF_XET_CACHE": str(Path(temporary) / "xet"),
            "HF_HUB_DISABLE_PROGRESS_BARS": "1",
            "PYTHONUNBUFFERED": "1",
        })
        command = ["uv", "run", "python", "-m", "src", "--output",
                   str(output / "results.json")]
        if args.suite != "public":
            if args.suite == "private":
                inputs = tests / "moulinette/private/input"
                definitions = inputs / "functions_definition.json"
                prompts = inputs / "function_calling_tests.json"
            else:
                definitions = tests / "changed_functions.json"
                prompts = tests / "changed_prompts.json"
            command += ["--functions_definition", str(definitions),
                        "--input", str(prompts)]
        started = time.monotonic()
        with (output / "install.log").open("w") as log:
            subprocess.run(["uv", "sync", "--frozen"], cwd=workspace,
                           env=environment, stdout=log,
                           stderr=subprocess.STDOUT, check=True)
        install_seconds = time.monotonic() - started
        if (workspace / "model").exists():
            raise RuntimeError("Model directory exists before the first run")
        events = []
        started = time.monotonic()
        with (output / "run.log").open("w") as log:
            process = subprocess.Popen(
                command, cwd=workspace, env=environment,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
            try:
                for line in process.stdout:
                    elapsed = time.monotonic() - started
                    events.append({"seconds": round(elapsed, 3),
                                   "message": line.rstrip()})
                    log.write(line)
                    log.flush()
                    print(line, end="", flush=True)
                status = process.wait()
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                process.stdout.close()
        elapsed = time.monotonic() - started
        metrics = {
            "platform": platform.platform(), "suite": args.suite,
            "source_sha256": hashes, "command": command,
            "model_cache_empty_before_run": True,
            "dependency_install_seconds": install_seconds,
            "first_run_wall_seconds": elapsed,
            "install_plus_first_run_seconds": install_seconds + elapsed,
            "downloaded_snapshots": [str(path.relative_to(workspace))
                                     for path in (workspace / "model").glob(
                                         "models--*/snapshots/*")],
            "exit_status": status, "events": events,
            "threads": {key: environment.get(key) for key in
                        ("OMP_NUM_THREADS", "MKL_NUM_THREADS")},
        }
        (output / "metrics.json").write_text(
            json.dumps(metrics, indent=2) + "\n",
        )
        print(f"First run including model download: {elapsed:.1f}s",
              flush=True)
        return status


if __name__ == "__main__":
    raise SystemExit(main())
