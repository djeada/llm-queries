# Evaluations

> **Status:** experimental

Reusable test suites for measuring whether an LLM or agent can complete a
concrete task reliably.

This directory is separate from `prompts/` and `local_setup_guides/`:

- a **prompt** is reusable input for doing a task
- a **guide** explains how to set something up
- an **evaluation** defines a task, expected behavior, and a scoring method

## Structure

- `specs/` — machine-readable JSONL evaluation cases
- `fixtures/` — deterministic response fixtures used to test the evaluator
- `tool-use/` — manual / agentic tool-use protocols
- `mcp/` — focused tests for MCP-connected applications such as Blender or ParaView
- `game-dev/` — cross-tool game-development pipeline evaluations
- `everyday/` — broader practical-task suites and source material for future
  executable cases

## Executable core suite

The repository includes a dependency-free runner:

```bash
python3 scripts/run_evals.py evaluations/specs/core.jsonl
```

With no model command or response file, that validates the specification.

To score captured responses:

```bash
python3 scripts/run_evals.py evaluations/specs/core.jsonl \
  --responses evaluations/fixtures/core-passing-responses.jsonl \
  --min-pass-rate 1
```

To run a local command that reads a prompt from stdin and writes the response to
stdout:

```bash
python3 scripts/run_evals.py evaluations/specs/core.jsonl \
  --command "ollama run <model:tag>" \
  --label "candidate-model" \
  --meta model="<model:tag>" \
  --meta runtime="ollama <version>" \
  --meta hardware="<machine description>" \
  --output results/core.json
```

The runner does not know about a model vendor. Any wrapper command can be used,
including scripts that call hosted APIs or agent harnesses.

Reports include the evaluation-spec SHA-256 and current Git commit so results
can be tied back to the exact benchmark definition.

## Compare two runs

```bash
python3 scripts/compare_eval_reports.py \
  results/baseline.json \
  results/candidate.json \
  --require-same-spec
```

The comparator reports case-level regressions, improvements, and score changes.
It exits nonzero when a case that passed in the baseline fails in the candidate.
Use `--require-same-spec` when you want a strict apples-to-apples comparison.

## JSONL case contract

Each line in a spec is one JSON object:

```json
{
  "id": "unique-case-id",
  "category": "coding-debugging",
  "prompt": "Prompt shown to the model",
  "checks": [
    {
      "type": "contains_all",
      "values": ["required phrase", "another phrase"]
    }
  ]
}
```

Supported deterministic checks:

- `exact`
- `contains_all`
- `contains_any`
- `contains_none`
- `regex`
- `json_keys`
- `max_chars`
- `line_count`
- `bullet_count`

These checks are intentionally simple and inspect observable output only. They
are useful for regression tests and instruction-following checks, not for
claiming a model has general intelligence.

## Evaluation contract

New evaluations should state:

1. **Capability under test**
2. **Setup / fixtures**
3. **Prompt or action**
4. **Expected observable behavior**
5. **Pass/fail criteria or scoring rubric**
6. **Known confounders**
7. **Results format**

Do not score hidden reasoning. Score outputs, tool calls, artifacts, state
changes, or other observable behavior.

For an end-to-end tool workflow example, see the
[Blender → Godot tiny RPG evaluation](game-dev/blender-godot-tiny-rpg.md).

## Result hygiene

A result should record enough context to reproduce the run:

- exact model identifier
- runtime / API version
- model configuration
- evaluation spec commit
- hardware when local
- tool permissions when agentic
- date and wall-clock timing
- failures and retries

Do not compare runs as equivalent when those conditions materially differ.

For the complete repository inventory, see [`CATALOG.md`](../CATALOG.md).
