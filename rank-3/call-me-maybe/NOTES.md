# Call me maybe

## Source inventory and scope

- Subject: `resources/subject.pdf`, **version 1.5**, all 21 pages read.
- Original supplied archives: `resources/llm_sdk.zip`, `resources/data.zip`.
- Evaluation screenshot: `resources/evaluation-sheet.png`, supplied 2026-10-09.
  Read completely alongside the version 1.5 subject; its issuing version and
  provenance are not independently verified.
- Evaluation PDF: `resources/evaluation-sheet.pdf`, supplied 2026-10-11.
  All four pages read. Title: `Intra Projects Call Me Maybe Edit`; the printed
  date is 2026-10-02. No scale version is stated. The original attachment was
  copied unchanged; its SHA-256 is
  `86fb68c31389c0f52206b3f8b2b6b12300783a4408754beafb8a8358d13fce81`.
- User-supplied tester: `resources/moulinette.zip` (original attachment
  `moulinette (1).zip`, received 2026-10-09). Its provenance is not verified as
  an official evaluation sheet; use it as additional testing evidence. Its
  public definitions and prompts match the supplied demonstration data.
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
- [x] Choose functions with the LLM; decode arguments from schema-constrained
  model scores with a finite preference for literal copying.
- [x] Mask invalid tokens before selection; enforce function names, all parameter
  keys, scalar types, escaping and JSON grammar during generation.
- [x] Support changed function definitions and prompts; no example-specific logic.
- [x] Successful batches contain exactly `prompt`, `name`, `parameters` for
  each prompt; rejected batches report an error and preserve existing output.
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
function definitions into standard Qwen tool schemas. It uses up to 48 tokens
of internal analysis, then selects a function and scalar argument values from
model logits under byte-aware JSON constraints. The internal analysis is never
written to the output file. Selected token IDs stay in the context; fixed field
prefixes are encoded using the public SDK. For strings, the best allowed initial
token is retained if it contains a complete quoted literal. Otherwise the known
opening quote is supplied before selecting content. This preserves whole empty
string tokens and the context used for longer values.
After the model starts a literal source prefix, matching continuations receive
a finite 3.5-logit preference at complete source-character boundaries.
A stronger model choice can generate a
derived string; the preference ends when that choice leaves the source text.
This improves punctuation preservation without requiring all strings to be
source substrings. It does not guarantee semantic correctness.

Token selection ranks model scores and checks only candidates that can still
win, preserving the exhaustive decoder's exact result and token-ID tie order.
Ordinary requests retain the original context and analysis. Explicitly announced
marker blocks use a constrained model task to identify delimiter labels from
the request, then present their content verbatim in a fresh argument context.
The output prompt stays unchanged. Quoted literals bypass block recognition;
there are no hardcoded delimiter pairs or function-specific extraction rules.

All output names and values come from constrained logits. JSON structure and
parameter keys come from the validated definitions. Final Pydantic checks verify
exact keys/types and scalar enums, and the complete batch is serialized before
output replacement. Declared numbers use floats only for lossless conversions;
integer and boolean arguments keep their exact types.
The model's internal `arguments` field becomes `parameters` in the required file.
No functions are executed, and no guessed fallback arguments are inserted after
a generation failure.
An internal rejection tool lets the model decline unrelated or incomplete
requests with a clear error. Its name is distinct from every supplied name.
The unchanged SDK stores actual model files in the local ignored `model/`
directory via `HF_HUB_CACHE`, set before SDK imports.

The flat mandatory schema supports string, number, integer, boolean and null.
Nested arrays/objects are bonus scope and will be rejected with a clear error.

## Submission inventory

`src/`, `pyproject.toml`, `uv.lock`, supplied `llm_sdk/`, supplied `data/input/`,
`Makefile`, `.gitignore`, `.flake8`, and the subject-required `README.md`.
Private checks and results live outside `submission/`.
The evaluation inventory contains 16 tracked files, including the SDK's three
original files and five authored source files. Local model files, the environment,
generated output and caches remain ignored development artifacts. A clean
standalone export excludes them; `uv sync` recreates its environment.

## Original validation and measured limitations (2026-09-13)

This section records the original implementation. Current fixes and fresh
measurements are recorded in the improvement validation section below.

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

## Simplification review (2026-10-09)

Review only: no files inside `submission/` were changed. The four implementation
modules contain 510 lines, plus the one-line package marker. Their separation
into command-line I/O, schemas, scalar grammar and model decoding is reasonable.
There is no framework, execution engine, retry system or bonus argument parser
to remove. Fixed JSON structure is already supplied directly; only function
names and scalar values need constrained model selection.

### Findings and recommended work

1. **Fix compatibility with the supplied grader first.** `decoder.py` returns
   the value of `json.loads`, so literals such as `2` become Python integers.
   `schema.py` correctly accepts integers or floats for JSON `number`, matching
   subject V.3.3. However, the tester's arithmetic functions explicitly assert
   `isinstance(value, float)`. Replaying `tests/supplied_results.json` therefore
   scores **7/11**, despite all calls passing the existing semantic checker.
   A diagnostic copy changing only six numeric values to floats scores **11/11**.
   The fresh additional set scores **8/11** raw and **10/11** after the same
   schema-driven float conversion. This is a grader compatibility issue rather
   than evidence that integers are invalid JSON numbers. A future patch should
   normalize only parameters declared `number`, preserve `integer`/`boolean`,
   and handle overflow and precision explicitly for large integers. Do not
   replace the existing exact-type and finite-number checks with blanket casts.

2. **Keep the current reasoning pass until its ambiguous-input behavior is
   preserved.** Removing it was much faster on ordinary inputs, but an empty
   request had not completed after **352.5 seconds**, when the experiment was
   terminated. Reducing its limit from 56 to 16 preserved the main test scores
   and roughly halved the additional-set runtime, but both ambiguous requests
   exceeded the experiment's 60-second per-prompt limit. The current 56-token
   implementation completed those exact requests in **14.5** and **13.8 seconds**.
   The experiments do not justify applying either shortcut as the default.
   All variants retained the same byte-aware grammar and SDK interface.

3. **Make small readability changes rather than restructure the modules.**
   `select_token()` and `reason()` duplicate logits conversion, shape validation
   and non-finite handling. A small shared helper could own those checks while
   each caller keeps its selection rules and context limit. Named constants
   would also explain the 256-value-token and context limits. These are modest
   cleanup opportunities, not reasons to introduce a base-class hierarchy or
   merge unrelated responsibilities. Keep the string-start branch: existing
   tests demonstrate why whole empty-string tokens and partial content need
   different handling. Keep byte-prefix checks for UTF-8 and JSON escapes.

4. **Retain the exposed string cases as semantic regressions.** In the fresh
   additional set, `Format template: Say "hello" to {name}` became
   `Say 'hello' to {name}` with the current code. The shorter variants added a
   trailing double quote instead. The two existing marker-delimited requests
   still retained `BEGIN`/`END` with the current model. Their JSON is valid, but
   their text is wrong. Refine a general preservation instruction and verify
   with the model before changing behavior; stripping punctuation or markers
   from arbitrary generated strings would damage legitimate inputs.

### Evidence and scoring

Fresh runs used Python 3.10.20, Apple M2 Pro / 16 GB RAM, cached
Qwen/Qwen3-0.6B, the unchanged supplied SDK and its public methods only.
Batch times below exclude model loading, which took 5.6-6.2 seconds per process.
The public baseline replay uses the previously saved model output; its inference
was not rerun with the 56-token budget during this review.

Semantic scores check the expected function name and behavior after converting
`number` arguments to floats **inside the tester only**. Changed-function and
marker cases use the existing exact expected arguments. Application outputs
were not corrected. The float diagnostic is explicitly separate from raw
model results.

| Decoder | Set | Semantic correctness | Completed valid calls | Batch time |
| --- | --- | --- | --- | --- |
| Current, 56 reasoning tokens | ZIP additional/private | 10/11 | 11/11 | 237.1 s |
| Current, 56 reasoning tokens | Existing edge cases | 0/2 scorable; 2 ambiguous | 4/4 | 63.9 s |
| No reasoning | ZIP public | 11/11 | 11/11 | 58.6 s |
| No reasoning | ZIP additional/private | 10/11 | 11/11 | 68.9 s |
| No reasoning | Existing changed functions | 10/10 | 10/10 | 37.5 s |
| No reasoning | Existing edge cases | Not scored; first request unfinished | 0 before termination | >352 s |
| 16 reasoning tokens | ZIP public | 11/11 | 11/11 | 95.1 s |
| 16 reasoning tokens | ZIP additional/private | 10/11 | 11/11 | 114.1 s |
| 16 reasoning tokens | Existing changed functions | 10/10 | 10/10 | 73.1 s |
| 16 reasoning tokens | Existing edge cases | 0/2 scorable; 2 ambiguous timeouts | 2/4 | 137.0 s |

The 60-second limit was imposed by the review harness, not by the application
or subject. No-reasoning was terminated after its first request exceeded the
subject's five-minute batch target. Partial experimental edge outputs are
labelled as partial; the actual application writes only a fully successful batch.

- `uv sync --frozen` succeeded in a standalone temporary copy.
- `make lint` passed flake8 and required mypy checks on all five source files.
- All 25 existing offline tests passed. They test structural correctness and
  errors; they do not catch the tester's float assertions or all semantic errors.
- Generated public and private definitions, prompts and corrections are kept
  under `tests/moulinette/{public,private}/`, outside the submission.
- Raw experiment outputs and `tests/moulinette/review_metrics.json` preserve
  the successful calls, timing measurements and incomplete cases.
- The tester scores matching function outputs, does not fully enforce the
  subject's exact schema, prints `PASSED` at 70%, and exits zero even for a
  failing score. Continue using independent schema checks and the subject's
  90% target; do not rely on its label or shell exit status alone.

### Reusing the supplied tests

From `submission/`, exercise the additional set with the unchanged application:

```sh
HF_HUB_OFFLINE=1 uv run python -m src \
  --functions_definition ../tests/moulinette/private/input/functions_definition.json \
  --input ../tests/moulinette/private/input/function_calling_tests.json \
  --output ../tests/moulinette/current_private_results.json
```

Run the original grader in a separate temporary environment so its dependencies
and generated files stay out of the submission:

```sh
moulinette_review_dir=$(mktemp -d)
unzip -q ../resources/moulinette.zip -d "$moulinette_review_dir"
uv run --project "$moulinette_review_dir/moulinette" --frozen python -m moulinette \
  grade_student_answers --student_answer_path ../tests/supplied_results.json --set public
uv run --project "$moulinette_review_dir/moulinette" --frozen python -m moulinette \
  grade_student_answers --student_answer_path ../tests/moulinette/public_float_diagnostic.json --set public
uv run --project "$moulinette_review_dir/moulinette" --frozen python -m moulinette \
  grade_student_answers --student_answer_path ../tests/moulinette/current_private_results.json --set private
```

The no-reasoning experiment replaced `Decoder.reason()` with only
`ids.extend(self.encode("\n</think>\n\n<tool_call>\n"))`. The 16-token experiment
changed only the reasoning loop's maximum iterations; termination handling and
all constrained decoding stayed intact. Neither experimental change was applied
to the submission.

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
- Explain the internal 48-token analysis and why its prose is not the final
  answer: the subsequent name/value tokens are always grammar-constrained.
- Explain the string-start decision: preserve a complete quoted-value token
  when the model selects it; otherwise supply the opening quote before choosing
  content. Always forcing the quote would exclude whole empty-string tokens.
- The mandatory solution does not support nested argument objects/arrays,
  execution, multiple-model selection, tokenization reimplementation, or
  application inference-result caching.
- Review all code and results with a peer before evaluation; compare the supplied
  evaluation screenshot with the current campus sheet. Private tests do not
  replace the official defense.

## Original resource SHA-256

```text
data.zip    04f766b6222f082d2d40ffb121349462085a912fd7a05c2cff2e5c1f022560a6
llm_sdk.zip b8387144c9944508ecde12a6977d4d80b34eef2cd68dc6cd343de5f30d241b66
subject.pdf 8b1f3af15abdece79f106233a8affcf4a7b8353d45444c14785776f7d2576507
moulinette.zip d5f8f4d63676246f44dfc227272a27c93df9083befa95d748b1b4c1f451d6e44
```

## Evaluation screenshot review (2026-10-09)

This records the state before the fixes. The checklist is updated as the gaps
are addressed; the original scores below remain historical measurements.

- [x] A standalone temporary copy passed `uv sync --frozen`, `make lint`, and
  all 25 offline tests. Fresh cached-model execution with the prescribed
  `uv run python -m src` entrypoint processed two prompts in 52.2 seconds.
- [x] Revalidated all 36 saved supplied, changed, private and edge outputs:
  exact prompt preservation, output keys, parameter keys and scalar types pass.
  This covers supported schemas, not unrestricted future definitions.
- [x] The supplied moulinette installed, prepared its private exercises, and
  replayed saved answers successfully: public 7/11, private 8/11. Both satisfy
  the screenshot's literal score-greater-than-zero check, but neither reaches
  its separate 90% accuracy target. These are grader replays, not fresh full
  inference runs.
- [x] Resolve float-only tester compatibility through lossless conversion of
  declared numbers. Integer and boolean arguments retain their types; very
  large or imprecise integers remain integers. Both forms satisfy the subject.
- [x] Enforce nonempty scalar enums during decoding and final validation.
  Invalid allowed-value types are rejected before model loading.
- [x] Store actual model weights and tokenizer files in the ignored local
  `model/` directory using public SDK integration and `HF_HUB_CACHE`.
  Local weights occupy 1,503,300,328 bytes; snapshot links resolve inside it.
- [x] Let the model select an internal rejection tool and report a clear error
  instead of forcing an unrelated supplied function. Unrelated, empty and
  ambiguous regression requests are rejected.
- [x] The completion fixes remove the unwanted markers in both original
  requests. Alternative marker names, tags, Unicode with inner quotes, and
  literal marker words also pass. See the 2026-10-10 validation below.
- [x] Rechecked broader accuracy and sampled repeatability: public 11/11 twice
  with byte-identical output, private 11/11, and changed functions 10/10.
  Quoted-template, letter-case and derived-regex cases also pass separately.
  Measured main batches finish within five minutes on this Mac. The marker
  original marker failures are addressed below; other hardware and arbitrary
  input sizes remain unverified. Optional bonuses remain outside the scope.

## Improvement validation (2026-10-09)

This section records the previous revision. The completion validation below
contains the current results; earlier failures and timings remain historical.

The implementation now supports scalar enums, rejects invalid allowed values
before model loading, and converts declared numeric integers to floats only
when their exact value survives conversion. This satisfies the supplied
tester's float assertions without changing integer or boolean parameters.
An internal rejection tool lets the model decline unmatched requests; its name
is kept distinct from supplied function names and never appears in output.

For strings, a finite 3.5-logit preference helps preserve literal text after the
model chooses a matching prefix. The initial check permits ASCII case
differences, so the preference can preserve the request's original spelling.
Bonuses require complete source-character boundaries, avoiding partial JSON
escapes and UTF-8 characters. A derived start receives no copy bonus; a stronger
derived continuation can leave the copied source. An earlier unconditional
first-token preference damaged generated regexes, which is why the final
selection keeps this gate. This is a semantic aid, not a guarantee of exact
extraction. The reasoning budget is 48 tokens.

The public SDK now uses `HF_HUB_CACHE` pointing to the ignored `model/`
directory. Cached weights were seeded from an existing download for these
offline runs; the application does not migrate global caches. Actual weights
occupy 1,503,300,328 bytes, and snapshot links resolve inside the project cache.
The supplied SDK and input data remain byte-identical to the original ZIPs.
Application imports and model access use only the SDK's public interface.

### Fresh batch results

These runs use Python 3.10.20, Apple M2 Pro / 16 GB, macOS 27.0, MPS,
Qwen/Qwen3-0.6B, and `HF_HUB_OFFLINE=1`. Times include model loading.

| Set | Correct calls | Schema and prompt preservation | Runtime | Raw supplied grader |
| --- | --- | --- | --- | --- |
| Public | 11/11 | 11/11 | 220.2 s | 11/11 |
| Public, final-source repeat | 11/11 | 11/11 | 217.2 s | 11/11 |
| Additional private | 11/11 | 11/11 | 294.4 s | 11/11 |
| Changed functions | 10/10 | 10/10 | 177.1 s | Independent checks |

The public measurement preceded an equivalent optimization that computes the
finite-token mask once per selection. The repeat, private and changed-function
runs used the final source. The repeat public output is byte-identical to the
first public output. Quoted-template, letter-case and regex cases also pass
in separate regressions. These are limited repeatability checks, not proof for
all possible inputs or hardware. Every measured main batch exceeds 90% semantic
accuracy and finishes within five minutes. The private set leaves only 5.6 seconds
of headroom; performance on other hardware and arbitrary request sizes is
unverified.

The unchanged supplied moulinette prepared its private exercises and scored
both public and private outputs 11/11. No tester-side float conversion was
used for these scores. This ZIP was supplied by the user; its official
provenance has not been established. Independent checks additionally enforce
exact function names, keys, scalar types, prompt preservation and expected
argument values. Equivalent regexes are scored by substitution behavior.

### Checks and remaining limits

- All 42 private offline tests pass, including enums, exact numeric conversion,
  rejection-name collisions, SDK cache setup, escaped source boundaries,
  original-case copying and derived regex starts and continuations.
- Flake8 and the required mypy flags pass. A fresh standalone submission copy
  passes `uv sync --frozen`, `make lint`, and `uv run python -m src --help`.
- A real CLI run with an unmatched request exits 1 with a clear error in
  20.274 seconds including model loading. An existing output file remains
  byte-identical and no temporary output file is left behind.
- The final 12 real-model regression checks pass 10/12: three expected
  rejections and seven of nine valid-call cases. All nine generated calls
  satisfy their schemas. Original and unseen quoted templates, enum arguments,
  lowercase names and two derived regex cases pass.
- The two marker-delimited messages still retain `BEGIN`/`END`. Backslashes
  and newlines survive, but the extracted text includes unwanted markers.
  These remain recorded semantic failures and are not counted as correct.

Results and source SHA-256 hashes are recorded in
`tests/moulinette/improvement_metrics.json` and
`tests/moulinette/improvement_probes.json`. Fresh batch outputs are
`fixed_public_results.json`, `fixed_private_results.json`, and
`fixed_changed_results.json` in that directory; the repeated public output is
`repeated_public_results.json`. Earlier unsuccessful revisions remain separately
labelled in the metrics and raw output files.

From `submission/`, rerun the private set with:

```sh
HF_HUB_OFFLINE=1 uv run python -m src \
  --functions_definition ../tests/moulinette/private/input/functions_definition.json \
  --input ../tests/moulinette/private/input/function_calling_tests.json \
  --output ../tests/moulinette/fixed_private_results.json
```

Run `uv run python ../tests/check_accuracy.py <output>` for public results,
adding `changed` for the changed-function set. The negative and stress harness
was `HF_HUB_OFFLINE=1 uv run python ../tests/run_evaluation.py`; its exit status
at this revision was 1 because of the two marker failures. All review fixtures
and results stay outside `submission/`. Optional bonuses remain out of scope.

## Completion validation (2026-10-10)

The final selector ranks finite logits with stable token-ID ties and rejects
illegal candidates before choosing one. During literal-copy scoring, it stops
only when a candidate's raw score plus the maximum 3.5 bonus cannot beat the
incumbent. This produces the same result as exhaustive masking, including ties;
it does not approximate selection with a fixed candidate count. Randomized
offline comparisons cover scalar grammars, enums, copied strings, invalid
scores and equal-score candidates.

Explicit marker blocks now use a constrained delimiter-identification task.
The recognizer accepts announced `between markers:`, `between X and Y:` or
`inside X and Y:` blocks, also allowing periods in place of colons. Quoted
regions are masked without changing character positions during recognition,
so literal marker phrases and quoted text before an instruction are preserved.
The LLM selects opening and closing labels from tokens present in the request;
no delimiter pairs, payloads or exercise names are hardcoded.

The nearest opening label before the last closing label identifies the block.
One separating ASCII space beside each word marker is omitted; additional
spaces and interior line breaks remain content. Punctuation/tag boundaries
preserve interior spaces. The content is presented verbatim in a fresh context
for the already selected function. Final argument values still come from
constrained logits, and the output keeps the original prompt unchanged.
Invalid marker locations produce a clear error instead of a fabricated value.

Ordinary requests retain their original context and 48-token analysis.
Experiments with general boundary classification and smaller ordinary contexts
caused semantic regressions, so neither is retained. Escaping the extracted
payload as a JSON string also damaged Unicode with inner quotes; the final
context uses the literal content instead. These choices keep the mandatory
solution within five source files and add no dependencies or bonus features.

### Fresh complete batches

Python 3.10.20, Apple M2 Pro / 16 GB, macOS 27.0, supplied SDK using MPS,
Qwen/Qwen3-0.6B, cached local weights and `HF_HUB_OFFLINE=1`.
All timings include model loading.

| Set | Correct calls | Valid schema / preserved prompts | Runtime | Margin below five minutes |
| --- | --- | --- | --- | --- |
| Public | 11/11 | 11/11 | 191.4 s | 108.6 s |
| Additional private | 11/11 | 11/11 | 234.7 s | 65.3 s |
| Changed functions | 10/10 | 10/10 | 167.6 s | 132.4 s |

The unchanged supplied moulinette scores both public and private results
11/11 without any tester-side numeric conversion. Independent checks enforce
function names, exact keys, scalar types, input prompt preservation and expected
arguments; equivalent public regexes are compared by substitution behavior.
All three output files are byte-identical to the earlier correct main batches.
The private run improves from 294.4 to 234.7 seconds, adding 59.7 seconds of
headroom. The measured main sets satisfy the 90% accuracy, 100% schema validity
and five-minute criteria. These measurements do not promise accuracy or runtime
for every unseen request, input size or machine.

### Current checks and reproduction

- All 47 private offline tests pass, including exhaustive-selection equivalence,
  preservation of ordinary contexts, arbitrary marker labels, quoted marker
  words, header offsets, whitespace and invalid marker locations.
- Flake8 and the required mypy flags pass on all five source files.
- A clean standalone export of the 16 evaluation files passes `uv sync --frozen`,
  `make lint` and `uv run python -m src --help` without sibling projects.
- The supplied SDK and input data remain byte-identical to the original ZIPs.
  Public SDK API usage, Pydantic inheritance, type hints and docstrings pass
  the final source audit. Model weights and local environments remain ignored.
- The final real-model regression run passes **17/17**: three expected
  rejections and fourteen correct, schema-valid calls. Both original marker
  requests, alternative names and XML/punctuation delimiters, Unicode with
  inner quotes, literal marker words, enums, quoted templates, letter case
  and derived regexes all pass with source hashes matching the final code.

Fresh answers are `tests/moulinette/completed_public_results.json`,
`completed_private_results.json`, and `completed_changed_results.json`.
`completion_metrics.json` records timings, output hashes and source hashes;
`completion_probes.json` records the current real-model stress checks.
Earlier `improvement_*` and review files remain historical evidence.

From `submission/`, check saved answers and run the current regressions:

```sh
uv run python ../tests/check_accuracy.py ../tests/moulinette/completed_public_results.json
uv run python ../tests/check_accuracy.py ../tests/moulinette/completed_private_results.json private
uv run python ../tests/check_accuracy.py ../tests/moulinette/completed_changed_results.json changed
HF_HUB_OFFLINE=1 uv run python ../tests/run_evaluation.py
```

## Evaluation study questions and answers (2026-10-11)

Source: the four-page `resources/evaluation-sheet.pdf`, subject version 1.5,
and the current application code. These are study questions derived from the
scale. They are not a list of questions guaranteed to be asked by an evaluator.
Keep this guide outside `submission/`. Read the answers first. Then practise
one question at a time without the answers.

### Requirement differences to resolve

- The scale's Output File Format section requires a JSON floating-point value
  for every parameter declared `number`, such as `2.0`, not `2`. Subject V.3.3
  permits integers or floats for `number`. The current implementation converts
  integers to floats only when conversion is exact. For example, `2**53 + 1`
  remains an integer. Thus, passing the recorded test sets does not establish
  compliance with the scale's stricter rule for every large number. Resolve
  this difference with the current campus requirements before changing the
  implementation. No numeric behaviour was changed during this study task.
- The scale names `data/output/function_calls.json` as the default. Subject V.4
  names `data/output/function_calling_results.json`. The program uses the subject
  name and supports an explicit `--output` path. Supply the requested path for
  the tester; do not claim the two default filenames are identical.
- The scale's moulinette check asks for a score above zero. Its separate
  accuracy requirements ask for at least 90%. A score above zero alone is not
  evidence that all mandatory requirements pass.

### Question bank

1. **What does this project do?**
   It converts a natural-language request into a function name and typed input
   arguments. It does not execute the function.

2. **What output is expected for "Add 2 and 3"?**
   One entry contains `prompt`, `name`, and `parameters`:

   ```json
   {"prompt": "Add 2 and 3", "name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
   ```

3. **Which files provide the functions and requests?**
   `data/input/functions_definition.json` provides definitions.
   `data/input/function_calling_tests.json` provides requests.

4. **How do you install and run the program?**
   From the submission root, run `uv sync`, then `uv run python -m src`.
   Use `--functions_definition`, `--input`, and `--output` for custom paths.

5. **What is the processing order?**
   Read options. Validate files. Load the model. Prepare each context. Select
   the function and arguments. Validate calls. Write the complete batch.

6. **What does each source module do?**
   `__main__.py` controls I/O and errors. `schema.py` validates data.
   `decoder.py` controls model generation. `grammar.py` checks candidate bytes.
   `__init__.py` identifies the package.

7. **What is the difference between a token and a token ID?**
   A token represents a piece of text. Its token ID is an integer identifying
   it in the vocabulary. Tokens need not be whole words or complete characters.

8. **What are logits?**
   They are raw next-token scores. Higher scores indicate greater preference.
   They are not probabilities. Softmax can convert them into probabilities.

9. **How does constrained decoding work in this code?**
   The decoder gets logits, ranks candidates, and rejects invalid byte
   continuations before selection. It selects the best permitted candidate.
   Eligible string-copy candidates can receive a finite score preference.
   Ranked rejection is equivalent to exhaustive masking for these rules.

10. **Why is the selected token ID added to the context?**
    The next model call must include what was already generated. Otherwise,
    the model receives the same input and can repeat the same selection.

11. **Can a number finish at `-2.`?**
    No. A decimal point needs at least one following digit. This prefix can
    continue as `-2.5`; a comma immediately after `-2.` is invalid.

12. **Can valid JSON contain incorrect arguments?**
    Yes. For "Add 2 and 3", `{"a": 8.0, "b": 9.0}` has valid types but
    incorrect values. Grammar controls structure; model interpretation can fail.

13. **Does function selection use keyword rules?**
    No. The model receives descriptions and requests. Its constrained scores
    select a name. Python restricts the available names; it does not select
    the function with rules such as `if "sum" in prompt`.

14. **What happens if function names or parameter names change?**
    The program reads the new definitions. No Python change is needed when
    the new definitions use the supported flat schema.

15. **Why use Pydantic?**
    The subject requires it for application classes. It checks structures and
    types. Strict validation prevents unwanted conversions and rejects extra fields.

16. **What is an enum and how is it enforced?**
    An enum lists permitted values. Input validation checks the list. Decoding
    restricts selection to those values. Final validation checks membership again.

17. **What format does the evaluation sheet require for `number` values?**
    It requires floating-point values such as `2.0`. Current code converts
    integers only when conversion preserves their exact value. Some large
    integers remain integers. See the unresolved requirement difference above.

18. **Why reject a boolean as a number?**
    Python booleans inherit from integers. Exact-type checks prevent `True`
    from satisfying a numeric parameter.

19. **Which model and SDK methods does the program use?**
    It uses Qwen/Qwen3-0.6B through `Small_LLM_Model`. It calls public `encode`,
    `get_logits_from_input_ids`, and `get_path_to_vocab_file` methods.
    It does not access private SDK attributes or methods.

20. **Why check bytes and complete token pieces?**
    A token can split a UTF-8 character or contain several JSON characters.
    Checking all candidate bytes preserves characters and rejects trailing junk.

21. **What do the generation constants control?**
    `CONTEXT_LIMIT=32768` limits context tokens. `VALUE_TOKEN_LIMIT=256` limits
    tokens for one generated value. `REASONING_TOKEN_LIMIT=48` limits internal
    analysis. `COPY_LOGIT_BONUS=3.5` prefers eligible literal-copy continuations.
    Token limits are not time limits. The copy preference is not a percentage.

22. **Where are the model files stored?**
    `MODEL_DIRECTORY` is `Path("model")`, relative to the working directory.
    The program sets `HF_HUB_CACHE` before importing the SDK. The downloaded
    files are ignored development artifacts.

23. **How are literal strings and marked text handled?**
    Eligible source-matching tokens receive a finite copy preference. Stronger
    choices can still generate derived text. For explicitly announced marker
    blocks, a constrained model task selects labels and the code locates content.
    The original output prompt is preserved.

24. **What happens with missing files, invalid JSON, or unmatched requests?**
    File validation happens before model loading. Errors print clear messages
    and return exit code 1. The model can select an internal rejection tool
    for unmatched requests. A failed batch preserves existing output.

25. **How is the output protected from partial writes?**
    All calls must succeed first. The program serializes the batch, writes a
    temporary file, then replaces the destination. Context managers close files;
    cleanup removes temporary files. Output cannot overwrite an input path.

26. **What should you say about accuracy and speed?**
    The targets are at least 90% accuracy, 100% valid successful JSON output,
    and a batch time below five minutes. Recorded cached-model batches passed
    11/11 public, 11/11 private, and 10/10 changed requests. Their times were
    191.4, 234.7, and 167.6 seconds on the measured Mac. These results do not
    guarantee correctness or speed for every request or machine.

27. **How do you run the supplied moulinette evaluation?**
    In its directory, run `uv sync` and
    `uv run python -m moulinette prepare_exercises --set private`.
    Run the application with the generated definitions and requests.
    Then run `uv run python -m moulinette grade_student_answers --set private
    --student_answer_path <answers-file>`. Read the score and also check schema
    compliance independently.

28. **Which checks demonstrate code quality?**
    `make lint` runs flake8 and the required mypy checks. Private unit tests
    check grammar, masking, validation, limits, and errors. Real-model checks
    separately examine function selection, argument values, and runtime.

29. **What must be in the evaluation repository?**
    Copy the evaluation-bound contents of `submission/`, including hidden
    configuration files. Include `src/`, `llm_sdk/`, `data/input/`, the Makefile,
    README, `pyproject.toml`, and `uv.lock`. Exclude generated output, model
    downloads, environments, caches, private tests, resources, and these notes.

30. **What small changes should you practise?**
    Explain and change a token limit. Run with a separate request file. Add
    a supported definition or enum in a separate file. Trace a generation
    failure to its error message. Recheck changed behaviour with relevant tests.
