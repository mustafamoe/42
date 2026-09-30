"""Provide the subject's command line interface and graceful error boundary."""

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

from src.schema import Call, load_inputs


def arguments() -> argparse.Namespace:
    """Parse the three required optional input and output paths."""
    parser = argparse.ArgumentParser(
        description="Translate requests into typed function calls."
    )
    parser.add_argument(
        "--functions_definition", type=Path,
        default=Path("data/input/functions_definition.json"),
    )
    parser.add_argument(
        "--input", type=Path,
        default=Path("data/input/function_calling_tests.json"),
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("data/output/function_calling_results.json"),
    )
    return parser.parse_args()


def write_calls(path: Path, calls: list[Call]) -> None:
    """Atomically replace the output only after the entire batch is valid."""
    content = json.dumps(
        [call.model_dump() for call in calls], ensure_ascii=True,
        indent=2, allow_nan=False,
    ) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=".function-calls-", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    """Validate, decode and write calls, returning nonzero on errors."""
    args = arguments()
    started = time.monotonic()
    try:
        if args.output.resolve() in {
            args.input.resolve(), args.functions_definition.resolve(),
        }:
            raise ValueError("Output must not overwrite an input file")
        functions, prompts = load_inputs(args.functions_definition, args.input)
        calls: list[Call] = []
        if prompts:
            from src.decoder import load_decoder

            print("Loading Qwen/Qwen3-0.6B...", file=sys.stderr, flush=True)
            decoder = load_decoder()
            for index, item in enumerate(prompts, 1):
                try:
                    calls.append(decoder.call(item.prompt, functions))
                except Exception as error:
                    raise ValueError(f"Prompt {index}: {error}") from error
                print(
                    f"Processed {index}/{len(prompts)}", file=sys.stderr,
                    flush=True,
                )
        write_calls(args.output, calls)
        elapsed = time.monotonic() - started
        print(
            f"Wrote {len(calls)} calls to {args.output} in {elapsed:.1f}s",
            file=sys.stderr,
        )
        return 0
    except KeyboardInterrupt:
        print("Error: interrupted; no new output was written", file=sys.stderr)
        return 130
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
