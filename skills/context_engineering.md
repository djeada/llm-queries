# Context Engineering

Use this prompt to decide what information an LLM should receive, how it should
be structured, and what should be omitted, summarized, retrieved, or placed in a
separate step.

## Best For

- Long-context tasks.
- Codebase, document, or research synthesis.
- Reducing hallucinations caused by missing or noisy context.
- Designing reusable prompt templates with source material.
- Deciding between stuffing context, summarizing it, or using retrieval.

## Required Input

- Task the model must perform.
- Available context or source types.
- Current prompt or workflow.
- Failure symptoms: missed facts, overfitting to examples, contradictions, or
  context overload.
- Output requirements and grounding rules.

## Prompt

```text
Act as a context engineering reviewer.

Design the context strategy for this LLM task. Decide what information should be
included, excluded, summarized, retrieved, or moved to another step.

Task:
"""
[WHAT THE MODEL MUST DO]
"""

Available context:
"""
[LIST DOCUMENTS, FILES, LOGS, EXAMPLES, USER DATA, POLICIES, OR KNOWLEDGE BASES]
"""

Current prompt or workflow:
"""
[PASTE CURRENT PROMPT OR DESCRIBE WORKFLOW]
"""

Observed problems:
"""
[MISSED FACTS, HALLUCINATIONS, VERBOSITY, CONTRADICTIONS, BAD CITATIONS]
"""

Output requirements:
"""
[FORMAT, CITATION RULES, LENGTH, TONE, ACCURACY REQUIREMENTS]
"""

Return:
1. Context inventory: include, exclude, summarize, retrieve, or ask user.
2. Recommended context order and section labels.
3. Grounding rules for how the model should use the context.
4. Missing context that blocks a reliable answer.
5. Compression strategy for long inputs.
6. Retrieval strategy if the context is too large or frequently changing.
7. Revised prompt skeleton with placeholders.

Rules:
- Prefer source-grounded answers when factual accuracy matters.
- Tell the model how to behave when context is incomplete or contradictory.
- Keep examples separate from instructions.
- Do not include sensitive or irrelevant data just because it is available.
```

## Follow-Up: Compress Context

```text
Compress this context for reuse in a prompt.

Context:
"""
[PASTE SOURCE MATERIAL]
"""

Task the compressed context must support:
"""
[TASK]
"""

Return:
1. Essential facts to preserve.
2. Details safe to omit.
3. Ambiguities or contradictions.
4. A compact context block.
5. Source labels or citation handles to keep.
```

## Review Checklist

- The context plan is tied to the actual task.
- Missing information is explicit.
- The model has rules for conflicting or insufficient context.
- The prompt separates instructions, source material, and examples.
