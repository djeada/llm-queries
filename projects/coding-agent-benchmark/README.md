# Coding Agent Benchmark

> **Status:** experimental

A small, provider-neutral benchmark for coding agents that edit a repository.

Each case contains a seed repository with a concrete issue. The harness copies
only that seed into a fresh workspace, initializes Git, sends the issue text to
an agent command, and scores the resulting workspace with checks kept outside
the copied repository.

The benchmark focuses on observable behavior:

- understand a bounded issue
- change the implementation rather than only explain it
- preserve existing behavior
- handle edge cases not fully covered by public tests
- avoid unrelated file churn
- leave a deterministically testable repository

## Initial cases

| Case | Failure class | Core behavior |
| --- | --- | --- |
| config-precedence | configuration semantics | CLI > environment > file > defaults |
| slug-normalization | text edge cases | stable ASCII slugs from messy input |
| cache-ttl | state/time semantics | expiry boundary, refresh, live-entry counting |

## Case isolation

Each case contains task.txt, seed/, evaluator.py, and golden/.

Only seed/ is copied into the agent workspace. The evaluator and golden files
remain outside the handed-off repository. This is useful for ordinary agent
testing, but it is not a secrecy model: someone with access to this benchmark
repository can read them.

## Requirements

- Python 3.11+
- Git
- no Python packages beyond the standard library

The agent itself is external to this project.

## Quick start

List cases with:

    python3 benchmark.py list

Prepare a fresh workspace:

    python3 benchmark.py prepare config-precedence /tmp/config-precedence

The prepared repository contains .benchmark-task.txt with the issue text.

After an agent or person edits the workspace:

    python3 benchmark.py score config-precedence /tmp/config-precedence

Run an stdin-driven agent wrapper end to end:

    python3 benchmark.py run config-precedence --command "my-agent-wrapper --stdin"

The wrapper runs with the prepared repository as its current directory and gets
the complete issue text on stdin. For another agent interface, use a small
wrapper that adapts stdin to that CLI/API.

## Output

score and run return JSON with:

- case ID
- pass/fail
- normalized score
- individual checks
- case-specific metrics
- Git changed files and working-tree status
- command exit information for run

A pass requires every evaluator check. Partial score is diagnostic; the
individual checks are the important result.

## Self-test

Run:

    make check

For every case the benchmark prepares the untouched seed and confirms it fails,
then overlays the known-good files from golden/ and confirms the same evaluator
passes.

This catches broken fixtures, accidentally fixed seeds, and impossible
evaluators.

## Run all cases

    python3 benchmark.py run-all --command "my-agent-wrapper --stdin" --output results/run.json

Each case receives its own temporary Git workspace.

## Fair comparisons

Record at least:

- agent/model
- agent/runtime version
- tool permissions
- benchmark commit
- operating system
- wrapper command
- timeout
- network policy
- retries
- human intervention

Keep case definitions and permissions equivalent between runs.

## Design principles

- **Observable behavior over prose:** explanations do not count if the repository remains broken.
- **Extra checks outside the workspace:** public tests are intentionally incomplete.
- **Tiny cases first:** small failures are easier to classify than large-repository failures.
- **Provider-neutral execution:** provider/model setup stays outside the benchmark.

## Adding a case

Add a focused task.txt, minimal seed repository, public validation, evaluator,
golden implementation, and deterministic offline scoring.

Prefer cases where a plausible shallow patch misses an important edge case.

Avoid style-only tasks, hidden requirements unrelated to the issue text, hidden
reasoning criteria, secrets, external services, and huge repositories whose
failures are difficult to classify.

## Known limitations

- Three tiny Python cases do not represent all software engineering.
- Extra evaluator checks are visible in this benchmark repository.
- Token usage is not measured unless an external wrapper reports it.
- Git diff size is descriptive, not automatically a quality score.
- Passing tests does not prove maintainability or security beyond the tested contract.
