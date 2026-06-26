# LLM Evaluation

Use this prompt to build a lightweight evaluation plan for prompts, models,
agents, or RAG workflows. It turns subjective output quality into test cases,
rubrics, failure categories, and regression checks.

## Best For

- Comparing prompt versions.
- Choosing between models for a task.
- Creating acceptance criteria before refactoring an LLM workflow.
- Catching regressions in format, accuracy, safety, or usefulness.
- Reviewing outputs from coding agents, assistants, or content workflows.

## Required Input

- Task being evaluated.
- Example inputs and expected qualities.
- Known failure modes.
- Constraints: sources, format, latency, cost, privacy, or safety.
- What counts as pass, partial pass, or fail.

## Prompt

```text
Act as an LLM evaluation designer.

Create a practical evaluation plan for this LLM workflow. The plan should be
small enough to run often but strong enough to catch meaningful regressions.

Workflow or task:
"""
[DESCRIBE THE PROMPT, AGENT, RAG PIPELINE, OR MODEL USE CASE]
"""

Expected behavior:
"""
[WHAT GOOD OUTPUT MUST DO]
"""

Known failure modes:
"""
[HALLUCINATIONS, FORMAT DRIFT, MISSING SOURCES, BAD TOOL USE, VERBOSITY, ETC.]
"""

Constraints:
- Sources allowed: [SOURCES OR NONE]
- Required output format: [FORMAT]
- Latency or cost limit: [LIMIT]
- Safety or privacy constraints: [CONSTRAINTS]
- Human review available: [YES/NO]

Return:
1. Evaluation goals.
2. Test case table with: case, input, expected behavior, failure it catches.
3. Rubric with scores from 1-5 for each quality dimension.
4. Pass/fail thresholds.
5. Regression checklist.
6. Human review instructions for borderline cases.
7. Minimal logging fields to capture for future debugging.

Rules:
- Include normal, edge, adversarial, and ambiguous cases.
- Test the output format separately from content quality.
- Do not rely only on vibes; define observable criteria.
- Keep the first version small enough to run manually.
```

## Follow-Up: Judge Outputs

```text
Evaluate these outputs using the rubric below.

Rubric:
"""
[PASTE RUBRIC]
"""

Test inputs and model outputs:
"""
[PASTE INPUTS AND OUTPUTS]
"""

Return:
1. Score per output and rubric dimension.
2. Evidence for each score.
3. Failure categories.
4. Highest-priority fix.
5. Whether this version passes the stated threshold.
```

## Review Checklist

- Test cases cover common and high-risk failures.
- The rubric uses observable criteria.
- Pass thresholds are explicit.
- The eval can be rerun after a prompt, model, or retrieval change.
