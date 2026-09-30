*This project has been created as part of the 42 curriculum by mal-hall.*

# Call me maybe

## Description

Call me maybe translates natural-language requests into function names and typed
arguments using Qwen/Qwen3-0.6B. It writes one JSON array containing exactly
`prompt`, `name` and `parameters` for each request. It never executes functions.

The mandatory implementation supports flat `string`, `number`, `integer`,
`boolean` and `null` parameters, including functions without parameters. Function
names, argument names, descriptions and types come from the input definitions.
Nested argument schemas are outside this implementation's scope.

## Instructions

Install [uv](https://docs.astral.sh/uv/) and run these commands from the project
root, which contains `src/` and `pyproject.toml`:

```sh
uv sync
uv run python -m src
```

The project requires Python 3.10; uv installs NumPy, Pydantic, the supplied local
SDK and development checks from the lockfile. The SDK depends on PyTorch,
Transformers and Hugging Face Hub. Application code uses the public SDK interface;
it does not directly import those inference libraries. The Transformers version
constraint ensures support for Qwen3 while retaining the supplied SDK's API.
Accelerate is installed for the SDK's automatic CUDA device mapping; application
code does not import it. The supplied SDK omits this conditional dependency.

The first model load needs internet access to download model files into the
normal Hugging Face cache. Allow several GB of disk space for the environment
and model. The unchanged SDK selects MPS on supported Macs, CUDA when available,
or CPU. Model loading or download errors produce a clear message and exit code 1.

After all model files have been downloaded, cached inference can run without
network lookups using the SDK dependency's standard offline setting:

```sh
HF_HUB_OFFLINE=1 uv run python -m src
```

This setting cannot download missing model files. CPU and CUDA execution were
not benchmarked on the development Mac; the reported timings use MPS.

Default input files:

- `data/input/functions_definition.json`
- `data/input/function_calling_tests.json`

Default output: `data/output/function_calling_results.json`. The parent directory
is created when writing. Output directories are excluded from Git.

The Makefile provides `install`, `run`, `debug`, `clean` and `lint`. Debugging uses
Python's built-in `pdb`. Run `make lint` for flake8 and the subject's mypy flags.
The supplied SDK is preserved verbatim and excluded from checks on authored code.

## Example usage

```sh
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/custom_calls.json
```

For `What is the sum of 2 and 3?`, one output entry is:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": {"a": 2, "b": 3}
}
```

Paths are relative to the current working directory unless absolute. Progress and
errors go to standard error. An empty prompt array produces `[]` without loading
the model. Malformed files, duplicate keys or names, unsupported argument types,
and invalid output paths fail clearly. Output cannot overwrite either input.
An unsuccessful batch leaves an existing output file unchanged.

## Algorithm explanation

1. Parse both JSON files and validate their exact structure with Pydantic.
2. Load the model and its vocabulary through `Small_LLM_Model` public methods.
   Convert vocabulary display characters back to their underlying bytes. This
   preserves BPE pieces that contain only part of a UTF-8 character. Actual
   tokenization still uses the SDK's `encode` method.
3. Convert the flat definitions into standard tool schemas with `properties` and
   `required` fields. Present them inside Qwen's `<tools>` chat format. This is
   prompt construction through the SDK, not a call to a tool-execution framework.
4. Allow up to 56 internal reasoning tokens before starting the tool call. Stop
   earlier if the model finishes thinking. This short analysis helps distinguish
   requested input values from computed results and derived patterns. It is not
   written to the output file. Only this internal analysis is unconstrained.
5. Supply `<tool_call>` and the fixed opening `{"name":`. Constrain the next value
   to a JSON-quoted name from the supplied functions.
   At every step, inspect each vocabulary token: appending its bytes must leave
   a prefix of an allowed name and the following comma. All other logits are
   negative infinity. Choose the highest remaining finite logit and append its
   token ID to the model context. The LLM therefore chooses the function.
6. Keep the selected token IDs in the context and append each fixed parameter
   key in definition order using the SDK tokenizer. Generate each value using
   its scalar grammar. For strings, first consider the best allowed initial
   token: retain it if it contains a complete quoted literal; otherwise supply
   the structural opening quote and select the content from that context.
   This preserves whole empty-string tokens while conditioning longer content
   on the known opening quote.
   String rules handle quotes, control characters, escapes, `\uXXXX` sequences
   and partial UTF-8 characters. Number rules reject leading zeros, incomplete
   decimal/exponent endings and non-finite results. Boolean and null rules allow
   only their exact JSON spellings. Integer rules exclude decimals and exponents.
7. Each value includes its terminating comma or brace. Tokens can contain several
   characters, including that delimiter, but cannot inject another field or prose.
   Prefix checks enforce syntax; completion checks also reject non-finite numbers.
8. Validate the complete call again against the selected function. Map the model's
   internal `arguments` object to the subject's required `parameters` field.
   Serialize the batch with `allow_nan=False`, then replace the output through
   a temporary file.
   The original prompt is copied directly from validated input.

Known structural text does not need model inference: it is fixed by the schema.
Every output name and value is chosen from constrained model logits. The
program does not repair arbitrary free-form model output or guess function names
from keywords.

The reasoning step and prompt aid interpretation; the scalar grammar and fixed
structure enforce output validity. No test answers appear in application code.

## Design decisions

- Five small source files separate validation, prefix grammar, model interaction
  and command-line I/O, with `__init__.py` marking the package.
- Every application class derives from Pydantic `BaseModel`. Strict validation
  prevents conversions such as `"3"` to a number or `true` to integer `1`.
- Greedy decoding makes selection simple and reproducible for a given logits
  sequence. There is no retry pipeline, model fine-tuning, batching or KV cache.
- A bounded reasoning pass improves interpretation before constrained generation.
  Its 56-token limit balances extraction accuracy against the runtime target.
- The SDK itself recomputes the full context on each logits request. No private
  SDK attributes or methods are accessed to bypass that interface.
- Generation stops with an error after 256 tokens for one value or when context
  reaches 32,768 tokens. It never inserts a fabricated fallback argument.
- All prompts must succeed before output is replaced. Standard-library context
  managers close files, and temporary files are cleaned even if writing fails.

## Performance analysis

Real-model measurements on 2026-09-13: Apple M2 Pro, 16 GB RAM, macOS,
Python 3.10, the supplied SDK using MPS, with model files already downloaded.

| Test set | Correct calls | Schema-compliant calls | Runtime |
| --- | --- | --- | --- |
| Supplied prompts | 11/11 (100%) | 11/11 | 272.5 seconds |
| Changed functions and prompts | 10/10 (100%) | 10/10 | 231.4 seconds |
| Additional edge cases | 0/2 scorable; 2 ambiguous | 4/4 | 90.7 seconds |

Both batches met the subject's 90% accuracy and five-minute targets on this
machine. Runtime includes model loading, with cached weights and
`HF_HUB_OFFLINE=1`. The test sets are small and do not establish accuracy on every
unseen function set.

The two marker-delimited stress requests failed exact text extraction: the model
kept `BEGIN`/`END` in the saved messages. The backslash and newline themselves
were preserved. These failures remain in the recorded results. Across all
scorable requests the result was 21/23 (91.3%), with 25/25 schema-compliant calls.
The two ambiguous requests are checked for schema compliance only.

Structural validity and semantic accuracy are different: a valid typed argument
can still contain the wrong text. Constraints guarantee the shape of successful
output, not interpretation of every possible request. Missing or ambiguous
arguments may be inferred incorrectly by the small model. Model downloads and
hardware differences affect runtime; the first download is not part of the
reported processing time.

Masking visits the vocabulary for each structured-output token. For vocabulary size V,
generated length T and maximum scalar byte length L, the straightforward prefix
checks cost O(T * V * L), apart from model inference. Internal reasoning adds at
most 56 model calls per prompt. Memory holds the model,
vocabulary, current context and completed calls. Finite generation limits bound
runaway continuation; they do not promise completion for arbitrary input sizes.

## Challenges faced

- BPE tokens are byte sequences, not whole words or necessarily whole Unicode
  characters. Byte-based grammar checks avoid corrupting multilingual strings.
- Token boundaries affect the model's next choice. Always forcing an opening
  quote excludes tokens representing an entire quoted value. Always selecting
  a partial opening token can instead change the context for longer content.
  The string-start rule handles both cases, with explicit regression tests for
  whole empty-string tokens and content selected after the opening quote.
- A token can close a string and add punctuation in one step. Checking the entire
  candidate piece prevents accepting an otherwise valid prefix with trailing junk.
- JSON numbers have incomplete intermediate states such as `-`, `1.` and `2e-`.
  Prefix and completion checks are separate so these can be continued safely.
- Valid JSON alone does not ensure correct extraction. Real-model checks score
  argument content separately from parsing and type compliance. Direct greedy
  JSON generation made semantic mistakes despite valid syntax. The final design
  uses Qwen's native tool format and a short internal analysis before masking
  names and arguments.

## Testing strategy

Twenty-five private tests are kept outside the evaluation repository. They
exercise valid scalar prefixes at every byte boundary, malformed escapes and
numbers, partial Unicode, random escaped strings, token masking against higher
invalid logits, non-finite logits and generation limits. File and CLI checks
cover malformed input, schema mismatches, empty batches, failure cleanup and
preserving existing output. Separate checks verify reasoning termination, its
token budget, and rejection of non-finite reasoning logits.

Real-model validation uses the supplied inputs and a separate changed function
set with multiplication, message storage, reminders, null and zero-argument calls.
Expected calls are recorded independently of application code. Regex arguments
are scored by substitution behavior, allowing equivalent patterns.
Additional stress cases check empty and ambiguous requests, backslashes and
newlines inside marker-delimited text; semantic failures are reported separately.

To check a standalone submission:

```sh
make lint
uv run python -m src
uv run python -m json.tool data/output/function_calling_results.json
```

Then compare each name, every argument and its type against the definitions and
the request. Python booleans must not be accepted as numbers when checking types.
Repeat with edited input files to verify that selection is not hardcoded.

## Resources

- [RFC 8259: JSON](https://www.rfc-editor.org/info/rfc8259/) - JSON grammar,
  strings and numbers.
- [Python JSON documentation](https://docs.python.org/3/library/json.html) -
  parsing, serialization and strict handling of non-finite numbers.
- [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B) - model context,
  chat format and reasoning behavior.
- [Qwen's shipped chat template](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/tokenizer_config.json)
  - tool schemas, role boundaries and the internal `arguments` field.
- [Pydantic configuration](https://docs.pydantic.dev/latest/api/config/) - strict
  type validation and rejecting extra fields.
- [uv project guide](https://docs.astral.sh/uv/guides/projects/) - dependency
  locking and project execution.
- [Hugging Face offline setting](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables#hfhuboffline)
  - using already-downloaded model files without network lookups.
- The supplied subject, version 1.5, and the original `llm_sdk` package define the
  project requirements and allowed inference interface.

AI assistance: Codex was used to extract the subject requirements, design and
implement the scalar decoder, create private checks, run model experiments, and
draft this documentation. The supplied SDK and demonstration inputs were copied
unchanged. Understanding, peer review and defense of the submitted implementation
remain the student's responsibility.
