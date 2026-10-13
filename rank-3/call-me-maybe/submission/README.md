*This project has been created as part of the 42 curriculum by mal-hall.*

# Call me maybe

## Description

Call me maybe translates natural-language requests into function names and typed
arguments using Qwen/Qwen3-0.6B. It writes one JSON array containing exactly
`prompt`, `name` and `parameters` for each request. It never executes functions.

The mandatory implementation supports flat `string`, `number`, `integer`,
`boolean` and `null` parameters, including functions without parameters. Function
names, argument names, descriptions and types come from the input definitions.
Scalar parameters can declare a nonempty `enum` of allowed values; these choices
are enforced during decoding and checked again before writing output.
Nested argument schemas are outside this implementation's scope.

## Instructions

Install [uv](https://docs.astral.sh/uv/) and run these commands from the project
root, which contains `src/` and `pyproject.toml`:

```sh
uv sync
uv run python -m src
```

On a 42 computer with `/goinfre`, use the Makefile first:

```sh
make install
make run
```

The Makefile automatically uses `/goinfre/$(id -un)/call-me-maybe`. It moves
existing `.venv/`, `model/` and `data/output/` directories there and leaves
symlinks at their original paths. Existing weights and results are preserved;
the ordinary `uv run python -m src` command and default output path still work.
uv's package cache, managed Python downloads and Hugging Face auxiliary cache
also use `/goinfre` during Makefile commands. No activation is necessary.

Storage belonging to another checkout is never merged or overwritten. To use
a different directory, pass `GOINFRE=/absolute/path` to each Makefile command.
Without `/goinfre`, the layout stays local; `GOINFRE=` disables automatic
relocation without moving existing links back. `make storage` performs only
the relocation. This storage is local to
the school computer and may be cleared: save results elsewhere before leaving,
and rerun `make install` and `make run` if the environment or model disappears.

The project requires Python 3.10; uv installs NumPy, Pydantic, the supplied local
SDK and development checks from the lockfile. The SDK depends on PyTorch,
Transformers and Hugging Face Hub. Application code uses the public SDK interface;
it does not directly import those inference libraries. The Transformers version
constraint ensures support for Qwen3 while retaining the supplied SDK's API.
Accelerate is installed for the SDK's automatic CUDA device mapping; application
code does not import it. The supplied SDK omits this conditional dependency.

The first model load needs internet access to download model files into the
local `model/` directory. Before importing the unchanged SDK, the application
sets the documented `HF_HUB_CACHE` variable to this directory. It contains real
cached weights and tokenizer files and is excluded from Git. Allow several GB
of disk space for the environment and model. The SDK selects MPS on supported
Macs, CUDA when available, or CPU. Loading or download errors exit clearly.

After all model files have been downloaded, cached inference can run without
network lookups using the SDK dependency's standard offline setting:

```sh
HF_HUB_OFFLINE=1 uv run python -m src
```

This setting cannot download missing model files. The performance section
distinguishes MPS and CPU measurements. CUDA was not benchmarked.

Default input files:

- `data/input/functions_definition.json`
- `data/input/function_calling_tests.json`

Default output: `data/output/function_calling_results.json`. The parent directory
is created when writing. Output directories are excluded from Git.

The Makefile provides `install`, `run`, `debug`, `clean`, `lint` and `storage`. Debugging uses
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
  "parameters": {"a": 2.0, "b": 3.0}
}
```

Paths are relative to the current working directory unless absolute. Progress and
errors go to standard error. An empty prompt array produces `[]` without loading
the model. Malformed files, duplicate keys or names, unsupported argument types,
and invalid output paths fail clearly. Output cannot overwrite either input.
An unsuccessful batch leaves an existing output file unchanged.
Before model loading, a temporary write checks the output filesystem. An
already full or unwritable output location fails early. This check does not
reserve space for the final result.
When the model selects rejection because no available function fits, the
program reports `No available function matches this prompt` and exits 1.

## Algorithm explanation

1. Parse both JSON files and validate their exact structure with Pydantic.
2. Load the model and its vocabulary through `Small_LLM_Model` public methods.
   Convert vocabulary display characters back to their underlying bytes. This
   preserves BPE pieces that contain only part of a UTF-8 character. Actual
   tokenization still uses the SDK's `encode` method.
3. Convert the flat definitions into standard tool schemas with `properties` and
   `required` fields. Present them inside Qwen's `<tools>` chat format. This is
   prompt construction through the SDK, not a call to a tool-execution framework.
   Add an internal rejection tool for requests that cannot be fulfilled. Its
   name is made distinct from supplied names; it never appears in output.
4. Encode the complete assistant prefix `<think>\n\n</think>\n\n` with the
   request in one tokenizer call. This is the prefix from Qwen's published chat
   template for `enable_thinking=False`. The SDK exposes raw tokenization rather
   than that option, so the application builds the documented template itself.
   No analysis tokens or effort-classification calls are generated. Blank
   requests fail before model work. The model still selects every function name
   and argument through constrained logits.
5. Supply `<tool_call>` and the fixed opening `{"name":`. Constrain the next value
   to a JSON-quoted supplied name or the internal rejection name. Selecting
   rejection raises a clear error before generating arguments.
   Rank finite scores, keeping token IDs in ascending order when scores tie.
   A candidate's bytes must leave a prefix of an allowed name and the following
   comma. Reject invalid candidates before selection. The first valid candidate
   is the exact highest-scoring legal token, without scanning lower-scoring
   tokens that cannot win. The LLM therefore chooses the function.
   When the generated prefix identifies exactly one allowed name, encode its
   remaining text through the public SDK without another logits request.
   The same rule applies to enum values and marker labels. It waits until a
   UTF-8 character is complete and respects the value and context token limits.
6. Keep the selected token IDs and original context for ordinary requests.
   For explicitly announced marker blocks, first ask the model to identify the
   opening and closing labels from tokens present in the request. Present the
   enclosed content verbatim after the instruction in the argument context, leaving
   the original output prompt unchanged. This fresh argument context contains
   only the selected tool and the extracted request.
   The function has already been selected by the model; argument values still
   come from constrained model logits.
   The block recognizer accepts `between markers:`, `between X and Y:`, and
   `inside X and Y:` (also periods instead of colons). It ignores phrases inside
   quoted literals. Delimiter names and payloads are not hardcoded. Word markers
   consume one separating space on each side; additional spaces and interior
   newlines remain content. Punctuation and tag markers preserve interior spaces.
   Append each fixed parameter key in definition order using the SDK tokenizer.
   Generate each value using
   its scalar grammar. For strings, first consider the best allowed initial
   token: retain it if it contains a complete quoted literal; otherwise supply
   the structural opening quote and select the content from that context.
   This preserves whole empty-string tokens while conditioning longer content
   on the known opening quote.
   After the model starts copying a literal source prefix, give matching
   continuations a finite 3.5-logit preference.
   The model's preferred token activates this check; ASCII case variants can
   identify a literal prefix while preserving its original spelling. A derived
   start that does not match the source keeps its unmodified model scores.
   The preference applies at complete source-character boundaries; unfinished
   escapes and split UTF-8 characters remain valid without receiving a bonus.
   A stronger model choice can extend the prefix into a derived string; once
   it leaves the source text, the copying preference stops. This preference
   improves punctuation preservation but does not guarantee exact extraction.
   Candidate scanning stops only when its raw score plus the maximum copy bonus
   cannot beat the current best score. This preserves exhaustive selection,
   including tie behavior; there is no fixed top-k approximation.
   String rules handle quotes, control characters, escapes, `\uXXXX` sequences
   and partial UTF-8 characters. Number rules reject leading zeros, incomplete
   decimal/exponent endings and non-finite results. Boolean and null rules allow
   only their exact JSON spellings. Integer rules exclude decimals and exponents.
   When a parameter has an `enum`, only JSON spellings of its allowed values and
   the terminating punctuation are possible, regardless of other token scores.
7. Each value includes its terminating comma or brace. Tokens can contain several
   characters, including that delimiter, but cannot inject another field or prose.
   Prefix checks enforce syntax; completion checks also reject non-finite numbers.
8. For declared `number` arguments, represent integers as floats only if their
   value survives the conversion exactly. Very large or imprecise integers stay
   integers; declared `integer` and `boolean` arguments are unchanged. Both forms
   are valid JSON numbers, while ordinary floats also satisfy float-only testers.
   Validate the complete call against the selected function and allowed values.
   Map the model's
   internal `arguments` object to the subject's required `parameters` field.
   Serialize the batch with `allow_nan=False`, then replace the output through
   a temporary file.
   The original prompt is copied directly from validated input.

Known structural text does not need model inference: it is fixed by the schema.
The model selects between permitted alternatives. Once only one finite choice
matches its generated prefix, the schema fixes the remaining text. Other values
continue through constrained model logits. The program does not repair arbitrary
free-form output or guess function names from keywords.

The model and prompt determine interpretation; the scalar grammar and fixed
structure enforce output validity. No test answers appear in application code.

## Design decisions

- Five small source files separate validation, prefix grammar, model interaction
  and command-line I/O, with `__init__.py` marking the package.
- Every application class derives from Pydantic `BaseModel`. Strict validation
  prevents conversions such as `"3"` to a number or `true` to integer `1`.
- Refusal is an LLM-selected tool choice, not a keyword rule or guessed fallback.
  A rejected prompt fails the batch without replacing any existing output.
- Greedy decoding makes selection simple and reproducible for a given logits
  sequence. There is no retry pipeline, model fine-tuning, batching or KV cache.
- Finishing a uniquely identified name or enum avoids redundant model calls.
  No decision between different allowed values is delegated to a keyword rule.
- Qwen's official non-thinking template avoids repeated SDK inference for
  internal analysis. This trades some semantic accuracy for lower latency;
  the measured losses are listed below. It also avoids a separate model call
  to classify the required effort.
- Explicit marker blocks use a short, constrained delimiter-identification
  task. Quoted literal messages bypass it. Ordinary requests retain their
  original model context.
- The SDK itself recomputes the full context on each logits request. No private
  SDK attributes or methods are accessed to bypass that interface.
- Generation stops with an error after 256 tokens for one value or when context
  reaches 32,768 tokens. It never inserts a fabricated fallback argument.
- All prompts must succeed before output is replaced. Standard-library context
  managers close files, and temporary files are cleaned even if writing fails.

## Performance analysis

Real-model measurements on 2026-10-13: Apple M2 Pro, 16 GB RAM, macOS 27.0,
Python 3.10.20, the supplied SDK using MPS, with model files already downloaded.

| Test set | Correct | Schema-compliant calls | Cached model, load + batch |
| --- | --- | --- | --- |
| Supplied public prompts | 11/11 | 11/11 | 44.4 seconds |
| Additional private prompts | 11/11 | 11/11 | 53.4 seconds |
| Changed functions and prompts | 9/10 | 10/10 | 30.7 seconds |
| Stress checks (including rejections) | 16/17 | 14/14 | 47.4 seconds |

Cached measurements isolate inference and loading with `HF_HUB_OFFLINE=1`.
They exclude downloads and are not the first-run acceptance test.

The prior adaptive decoder took 87.6 seconds on the public set using the same
Mac and cached weights. Non-thinking mode removes the effort decision and all
analysis-token inference: SDK calls fall from 293 to 125. This speedup applies
to inference during a first run too; it does not depend on persistent answers
or hidden model state.

A separate ordinary CLI run started with empty model and Hugging Face download
caches in an isolated copy. It took **149.5 seconds**, including uv/Python
startup, downloading weights, model loading, all 11 requests and output writing.
All 11 calls were correct. Including dependency setup, the total was 150.9
seconds; that setup reused uv's package cache. These are Mac MPS measurements,
not timings from the school CPU.

The user's school screenshot for the previous adaptive version reports 291.5
seconds with model downloads visible. The new version still needs a fresh
first-run measurement on that Linux computer. CPU thread limits are not forced;
the earlier four-thread result did not show an improvement. Network throughput,
hardware, machine load and longer inputs can affect the total. The Makefile's
`/goinfre` setup addresses the full-home-filesystem failure, and an early write
probe checks the output location before inference begins.

This version accepts a documented speed–accuracy tradeoff:

- The changed-function set scores 9/10: a message containing nested quotes has
  its quotes changed and retains unwanted wrapping quotes.
- The stress set scores 16/17, including all three expected rejections: a regex
  for `cat` followed by digits becomes `cat`, producing the wrong substitution.

All generated calls in these runs are schema-compliant. Every measured set
meets the 90% semantic threshold, but the changed set is exactly at the minimum.
These small sets do not establish accuracy on unseen evaluation inputs.
The previous decoder passed these two cases; the faster mode was selected with
this loss acknowledged. Structural validity does not guarantee correct meaning.
The CLI's printed elapsed time includes model downloads and loading; use an
external wall timer when also counting Python startup or dependency installation.

For a fixed schema, vocabulary size V, model-selected length T, maximum scalar
byte length L and K
candidates inspected per token, ranking and prefix checks cost
O(T * (V log V + K * L)), apart from model inference. K can be V in the worst
case, but ordinary requests usually inspect far fewer candidates.
No inference calls are spent on internal analysis. Memory holds the model,
vocabulary, current context, encoded copy source and completed calls. Literal
scoring also searches the request for each candidate, so longer requests add
work beyond the schema checks. Finite generation limits bound
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
  uses Qwen's native non-thinking tool format while masking names and arguments.
  This improves speed but retains the documented semantic limitations.

## Testing strategy

Sixty private tests are kept outside the evaluation repository. They
exercise valid scalar prefixes at every byte boundary, malformed escapes and
numbers, partial Unicode, random escaped strings, token masking against higher
invalid logits, non-finite logits and generation limits. File and CLI checks
cover malformed input, schema mismatches, empty batches, failure cleanup and
preserving existing output.
Evaluation regressions cover enum definitions and token masks, exact numeric
conversion, rejection without name collisions, local SDK cache setup, and both
copied strings and derived strings sharing a literal prefix.
Additional checks compare ranked selection with exhaustive masking across
random scores, ties and non-finite values, and verify ordinary tool contexts,
arbitrary delimiter labels, literal-marker preservation and content whitespace.
Further checks cover early output failures, completion only after finite choices
are disambiguated, split UTF-8, and both token limits during completion.
Non-thinking checks verify the complete prefix is tokenized together, no
analysis calls precede function selection, and blank requests fail immediately.
Makefile checks cover storage relocation, idempotency, conflicting destinations,
existing links, cleared storage and cache environment settings.

Real-model validation uses the supplied inputs and a separate changed function
set with multiplication, message storage, reminders, null and zero-argument calls.
Expected calls are recorded independently of application code. Regex arguments
are scored by substitution behavior, allowing equivalent patterns.
Additional stress cases check empty and ambiguous requests, backslashes and
newlines inside marker-delimited text, alternative delimiters and literal marker
words. Semantic accuracy is checked independently of JSON/schema validity.
The real-model stress run passed 16/17 checks: all three expected rejections
and thirteen correct calls. All fourteen generated calls are schema-compliant;
the complex regex case remains a semantic failure.

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
  - tool schemas, role boundaries, the internal `arguments` field and the
    complete non-thinking assistant prefix.
- [Pydantic configuration](https://docs.pydantic.dev/latest/api/config/) - strict
  type validation and rejecting extra fields.
- [uv project guide](https://docs.astral.sh/uv/guides/projects/) - dependency
  locking and project execution.
- [uv environment variables](https://docs.astral.sh/uv/reference/environment/) -
  placing package caches and managed Python installations in external storage.
- [Hugging Face offline setting](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables#hfhuboffline)
  - using already-downloaded model files without network lookups.
- [Hugging Face cache configuration](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables#hfhubcache)
  - locating downloaded model files in the project's `model/` directory.
- The supplied subject, version 1.5, and the original `llm_sdk` package define the
  project requirements and allowed inference interface.

AI assistance: Codex was used to extract the subject requirements, design and
implement the scalar decoder, create private checks, run model experiments, and
draft this documentation. The supplied SDK and demonstration inputs were copied
unchanged. Understanding, peer review and defense of the submitted implementation
remain the student's responsibility.
