# Call me maybe

## Source inventory and scope

- Subject: `resources/subject.pdf`, **version 1.5**, all 21 pages read.
- Original supplied archives: `resources/llm_sdk.zip`, `resources/data.zip`.
- No evaluation sheet was supplied.
- Python 3.10; mandatory work only. Nested arguments and other bonuses excluded.
- Original SDK copied unchanged to `submission/llm_sdk/`; demonstration inputs
  copied unchanged to `submission/data/input/`.
- SDK dependencies necessarily include torch/transformers/Hugging Face. The
  application must not import these libraries or use private SDK attributes;
  it interacts exclusively through the supplied public wrapper methods.
- Section V.4 specifies `data/output/function_calling_results.json`; this is the
  default output. Other names in the usage examples are custom output examples.
- README login follows the existing Rank 3 projects: `mal-hall`.

## Mandatory checklist

- [x] Preserve official inputs and initialize the required project layout.
- [x] Use Qwen/Qwen3-0.6B through public SDK methods only.
- [x] Choose functions and argument values using model logits, without heuristics.
- [x] Mask invalid tokens before selection; enforce function names, all parameter
  keys, scalar types, escaping and JSON grammar during generation.
- [x] Support changed function definitions and prompts; no example-specific logic.
- [x] Produce exactly `prompt`, `name`, `parameters` for every prompt.
- [x] Handle missing/malformed files, wrong types, empty strings, large numbers,
  special characters, ambiguous requests, and multiple parameters gracefully.
- [x] Provide `uv sync` and `uv run python -m src` with all three required flags.
- [x] Provide Makefile install/run/debug/clean/lint targets with required flags.
- [x] Use Pydantic validation for all application classes; type hints/docstrings.
- [x] Pass flake8 and required mypy checks on authored code.
- [x] Include required English README sections and AI-use disclosure.
- [x] Validate supplied prompts and unseen function sets with the real model.
- [x] Measure >=90% semantic accuracy, 100% valid schema-compliant JSON and
  runtime under five minutes on the measured test set.
- [x] Audit submission inventory and exclude output/caches/environments.

## Mandatory design

The application validates files before loading the model and converts the flat
function definitions into standard Qwen tool schemas. It uses up to 56 tokens
of internal analysis, then selects a function and scalar argument values from
model logits under byte-aware JSON constraints. The internal analysis is never
written to the output file. Selected token IDs stay in the context; fixed field
prefixes are encoded using the public SDK. For strings, the best allowed initial
token is retained if it contains a complete quoted literal. Otherwise the known
opening quote is supplied before selecting content. This preserves whole empty
string tokens and the context used for longer values.

All output names and values come from constrained logits. JSON structure and
parameter keys come from the validated definitions. Final Pydantic checks verify
exact keys/types, and the complete batch is serialized before output replacement.
The model's internal `arguments` field becomes `parameters` in the required file.
No functions are executed, and no guessed fallback arguments are inserted after
a generation failure.

The flat mandatory schema supports string, number, integer, boolean and null.
Nested arrays/objects are bonus scope and will be rejected with a clear error.

## Submission inventory

`src/`, `pyproject.toml`, `uv.lock`, supplied `llm_sdk/`, supplied `data/input/`,
`Makefile`, `.gitignore`, `.flake8`, and the subject-required `README.md`.
Private checks and results live outside `submission/`.
The final directory contains exactly the 16 files in this inventory, including
the SDK's three original files and the five authored source files. Generated
output, caches and the temporary virtual environment were removed after testing;
`uv sync` recreates the environment from the lockfile.

## Validation and measured limitations

Measured on 2026-09-13, Apple M2 Pro / 16 GB RAM / macOS 26.6.2, Python 3.10.20,
Qwen/Qwen3-0.6B through the unchanged SDK's MPS backend. Model files were already
downloaded. Timings include model loading.

| Dataset | Semantic accuracy | Valid/schema-compliant | Runtime |
| --- | --- | --- | --- |
| Supplied 11 prompts | 11/11 (100%) | 11/11 | 272.5 s |
| Changed 10 prompts / five new functions | 10/10 (100%) | 10/10 | 231.4 s |
| Four additional edge cases | 0/2 scorable; 2 ambiguous | 4/4 | 90.7 s |

Both main batches pass every expected call. Equivalent regexes are scored by
substitution behavior. Tests establish the measured thresholds on these sets,
not universal accuracy. Ambiguous requests have no unique semantic answer.

The edge-case scorer intentionally exits 1: both marker-delimited requests retain
`BEGIN`/`END`; the backslash and newline content itself is preserved. These
are unresolved semantic limitations, not JSON/schema failures. No postprocessing
hides them. Overall, 21/23 scorable requests pass (91.3%); all 25 outputs are
schema-compliant. The two ambiguous requests count only toward schema checks.
The graceful-handling checklist means these cases produce valid output or clear
errors; it does not claim every special-character request is interpreted exactly.

Actual outputs are preserved as `tests/supplied_results.json`,
`tests/changed_results.json`, and `tests/edge_results.json`. The measurements use
the downloaded model cache with `HF_HUB_OFFLINE=1`.

Direct-generation experiments exposed semantic mistakes despite valid JSON.
Qwen's native tool format and bounded internal analysis improved extraction,
especially regex requests, at the cost of more inference calls. The 56-token
reasoning limit keeps the measured supplied batch under five minutes. Separate
string-start regressions protect whole quoted literals and the context used for
longer content. No model output is executed.

- 25 private offline tests pass, including every-byte prefix checks, escapes,
  UTF-8 splits, invalid numbers, masking, finite logits, generation limits,
  malformed input, exact keys/types, output failure and cleanup. Reasoning
  termination and whole quoted-value tokens have explicit regression checks.
- `make lint` passes flake8 and the exact required mypy flags on all five
  authored Python files. The original SDK is excluded, not reformatted.
- A separate clean standalone copy passed `uv sync --frozen`, `make lint`, and
  `uv run python -m src --help`, verifying relative SDK dependency resolution.
- SDK files and demonstration inputs match their original ZIP entries byte for
  byte. Outputs, virtual environments and caches are excluded from Git.
- An AST audit confirmed Pydantic classes, docstrings, type annotations and no
  forbidden application imports or private attributes.
- `make debug` reached pdb and quit cleanly. The dependency lock includes
  Accelerate because the provided SDK's CUDA `device_map="auto"` path requires
  it; the SDK omitted that conditional dependency. CPU/CUDA were not benchmarked.
- A network lookup failure exited clearly and preserved output. Remaining model
  checks used the already-downloaded cache with `HF_HUB_OFFLINE=1`. This is a
  documented SDK dependency setting, not a custom application flag.

Commands, from `submission/`:

```sh
uv sync
make lint
uv run python -m unittest discover -s ../tests -v
uv run python -m src
uv run python ../tests/check_accuracy.py data/output/function_calling_results.json
uv run python -m src \
  --functions_definition ../tests/changed_functions.json \
  --input ../tests/changed_prompts.json \
  --output ../tests/changed_results.json
uv run python ../tests/check_accuracy.py ../tests/changed_results.json changed
uv run python -m src \
  --functions_definition ../tests/changed_functions.json \
  --input ../tests/edge_prompts.json \
  --output ../tests/edge_results.json
uv run python ../tests/check_accuracy.py ../tests/edge_results.json edge
```

Prefix model-running commands with `HF_HUB_OFFLINE=1` when using an already
complete cache without network access. The edge scorer's nonzero status records
the known exact-text failures above.

## Defense notes

- Explain the distinction between structural validity and semantic correctness.
  A string can be perfectly valid JSON while containing incorrect text.
- Walk through masking after the number prefix `-2.`: a digit can continue it;
  a comma cannot close it until the fractional part has a digit.
- Explain why `true` is rejected for a number even though Python's `bool`
  inherits from `int`; the final validator compares exact types.
- Show how a token containing `",` can finish a string and its separator, while
  a token containing trailing prose is rejected before selection.
- Explain why UTF-8 bytes must survive across token boundaries and why replacing
  incomplete bytes with the Unicode replacement character loses information.
- Function choice comes from model logits constrained to the provided names.
  The schema fixes parameter keys; it never selects function names by keywords.
- Changing a function set requires editing its JSON definitions, not Python code.
  Return types are validated metadata; the program never calls actual functions.
- Explain the internal 56-token analysis and why its prose is not the final
  answer: the subsequent name/value tokens are always grammar-constrained.
- Explain the string-start decision: preserve a complete quoted-value token
  when the model selects it; otherwise supply the opening quote before choosing
  content. Always forcing the quote would exclude whole empty-string tokens.
- The mandatory solution does not support nested argument objects/arrays,
  execution, multiple-model selection, tokenization reimplementation, or caching.
- Review all code and results with a peer before evaluation; no evaluation sheet
  was supplied, and private tests do not replace the official defense.

## Original resource SHA-256

```text
data.zip    04f766b6222f082d2d40ffb121349462085a912fd7a05c2cff2e5c1f022560a6
llm_sdk.zip b8387144c9944508ecde12a6977d4d80b34eef2cd68dc6cd343de5f30d241b66
subject.pdf 8b1f3af15abdece79f106233a8affcf4a7b8353d45444c14785776f7d2576507
```
