# Prompt Debugging

Use this prompt when an LLM produces vague, incorrect, overlong, brittle, or
inconsistent output. It diagnoses the prompt, identifies likely failure modes,
and rewrites it with a testable structure.

## Best For

- Improving unreliable prompt templates.
- Debugging hallucinations, verbosity, ignored constraints, or format drift.
- Converting vague instructions into a reusable workflow.
- Comparing two prompt versions against the same examples.

## Required Input

- Current prompt.
- Desired output.
- Bad output examples.
- Model or model family, if relevant.
- Constraints: length, tone, format, sources, tools, or forbidden behavior.

## Prompt

```text
Act as a prompt debugging specialist.

Diagnose why this prompt is failing and produce a stronger version. Focus on
instruction clarity, missing context, output contract, ambiguity, examples, and
testability.

Current prompt:
"""
[PASTE PROMPT]
"""

Desired output:
"""
[DESCRIBE WHAT GOOD OUTPUT LOOKS LIKE]
"""

Bad or disappointing output:
"""
[PASTE MODEL OUTPUT OR DESCRIBE FAILURE]
"""

Constraints:
- Model: [MODEL OR UNKNOWN]
- Audience: [AUDIENCE]
- Required format: [FORMAT]
- Length limit: [LIMIT]
- Must use these facts or sources: [SOURCES OR NONE]
- Must avoid: [FORBIDDEN CONTENT OR BEHAVIOR]

Return:
1. Diagnosis table with: issue, evidence, why it hurts output, fix.
2. The top 3 failure modes to test.
3. A rewritten prompt.
4. Optional examples or counterexamples to add.
5. A small test set with at least 5 cases.
6. Acceptance criteria for deciding whether the new prompt is better.

Rules:
- Do not make the prompt longer unless the added structure earns its place.
- Prefer clear output contracts over vague style words.
- Separate task instructions from examples and source material.
- If the desired behavior is impossible from the provided context, say so.
```

## Follow-Up: Compare Prompt Versions

```text
Compare these two prompt versions using the same test cases.

Prompt A:
"""
[PASTE VERSION A]
"""

Prompt B:
"""
[PASTE VERSION B]
"""

Test cases and outputs:
"""
[PASTE CASES AND OUTPUTS]
"""

Return:
1. Which version is better for each case.
2. Failure patterns.
3. Which instructions helped or hurt.
4. A merged version that keeps the strongest parts.
```

## Review Checklist

- The rewritten prompt has a clear role, task, inputs, rules, and output format.
- Failure modes are testable.
- The prompt tells the model what to do when information is missing.
- The output can be judged without guessing the author's intent.
