# IntentSpec — Software Supplement

Code and data for reproducing the experiments in the paper.

## Setup

```
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

## Reproducing results from cached generations (no API key needed)

Cached model completions are included under `data/generations/`, so the
following can be run without any API access:

```
python scripts/validate_benchmark.py
python compute_ci.py
python scripts/plot_ivr_distribution.py results/experiment1.json
```

## Running the full pipeline (requires an API key)

To regenerate solutions from scratch, set `ANTHROPIC_API_KEY` (for claude-*
models) or `OPENAI_API_KEY` (for gpt-*/o1-*/o3-*/codex-* models) in your
environment, then:

```
python scripts/run_experiment1.py
```

This loads spec pairs from `data/specs/spec_pairs.jsonl`, generates solutions,
evaluates them against stated and hidden constraints, and writes results to
`results/experiment1_{model}.json`.

## Layout

- `src/intentspec/` — core library (dataset loading, generation, execution,
  IVR computation, schema)
- `scripts/` — experiment entry points
- `data/specs/` — benchmark spec pairs and canonical reference solutions
- `data/generations/` — cached model completions used in the paper
- `tests/` — unit tests (`pytest`)
