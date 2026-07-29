# IntentSpec Benchmark — Data Supplement

This archive contains the benchmark data used to compute Intent Violation
Rate (IVR) in the paper: 49 tasks, each derived from a HumanEval problem and
extended with an ambiguous/gold prompt pair and a decomposed set of
executable constraints.

## Files

### `spec_pairs.jsonl`

The benchmark itself — one JSON object per line, one line per task. This is
the file consumed directly by the evaluation pipeline (`run_experiment1.py`,
`validate_benchmark.py` in the software supplement).

Fields:

| Field              | Type            | Description |
|---------------------|-----------------|-------------|
| `task_id`           | string          | HumanEval task identifier, e.g. `"HumanEval/26"`. Matches the `task_id` in `canonicals.jsonl`. |
| `spec_type`         | string          | Category of the task. Currently always `"algorithm"`. |
| `ambiguous_prompt`  | string          | The under-specified prompt a developer might plausibly write — states only some of the task's real constraints. |
| `gold_prompt`       | string          | The fully clarified version of the prompt, stating every constraint explicitly. |
| `constraints`       | list of objects | All atomic, executable constraints implied by the gold prompt (see below). |
| `stated_test_ids`   | list of strings | IDs (from `constraints`) that are mentioned, even implicitly, in `ambiguous_prompt`. |
| `hidden_test_ids`   | list of strings | IDs (from `constraints`) that appear only in `gold_prompt`, not in `ambiguous_prompt`. A solution that passes all `stated_test_ids` but fails one or more `hidden_test_ids` counts as an intent violation — this is what IVR measures. |

Each entry in `constraints` is an object:

| Field         | Type   | Description |
|---------------|--------|-------------|
| `id`          | string | Local constraint identifier (e.g. `"C1"`), referenced by `stated_test_ids`/`hidden_test_ids`. |
| `description` | string | Human-readable statement of the constraint. |
| `test_code`   | string | Executable Python snippet that calls `solution(...)` and asserts the constraint holds. Run by concatenating a candidate solution with this snippet and executing it; a zero exit code means the constraint passed. |

Example (abbreviated):

```json
{
  "task_id": "HumanEval/26",
  "spec_type": "algorithm",
  "ambiguous_prompt": "Write a function named `solution` that takes a list of integers and removes any elements that appear more than once.",
  "gold_prompt": "Write a function named `solution` that takes a list of integers, removes all elements that occur more than once, preserves the original order of remaining elements, and returns a new list without mutating the input.",
  "constraints": [
    {"id": "C1", "description": "Elements appearing more than once are removed", "test_code": "result = solution([1, 2, 3, 2, 4])\nassert 2 not in result"},
    {"id": "C2", "description": "Original order of remaining elements is preserved", "test_code": "..."},
    {"id": "C3", "description": "Input list is not mutated", "test_code": "..."},
    {"id": "C4", "description": "Empty list returns empty list", "test_code": "..."}
  ],
  "stated_test_ids": ["C1"],
  "hidden_test_ids": ["C2", "C3", "C4"]
}
```

### `canonicals.jsonl`

The original HumanEval reference (gold) solutions that `spec_pairs.jsonl`
was built from. Used for benchmark validation — confirming that a correct,
known-good solution passes every constraint (stated and hidden) for its
task, i.e. that IVR == 0 for canonical solutions.

Fields:

| Field                | Type   | Description |
|----------------------|--------|-------------|
| `task_id`            | string | HumanEval task identifier, matches `spec_pairs.jsonl`. |
| `entry_point`        | string | Name of the function under test in the original HumanEval problem. |
| `prompt`             | string | Original HumanEval function signature + docstring. |
| `canonical_solution` | string | Original HumanEval reference implementation body. |
| `full_source`        | string | `prompt` + `canonical_solution` concatenated into a runnable module. |

## Provenance and licensing

Both files are derived from **HumanEval**
(https://github.com/openai/human-eval), released by OpenAI under the
**MIT License**. `canonicals.jsonl` reproduces HumanEval's original prompts
and reference solutions verbatim (field-renamed for our pipeline).
`spec_pairs.jsonl` is new work built on top of HumanEval: for each of the 49
selected HumanEval tasks, we authored an ambiguous/gold prompt pair and a
decomposed set of constraint tests by hand, using the HumanEval problem
statement and reference solution as the source of ground truth. `task_id`
values (e.g. `"HumanEval/26"`) directly reference the corresponding upstream
HumanEval problem.

This derived data is released under the same MIT License as HumanEval, in
accordance with its terms.
