# Intro to Prompt Engineering

Prompt engineering is the practice of designing the information and
instructions given to a model so that its output is useful, checkable, and
appropriate for the task.

A good prompt is not magic wording. It is an interface specification.

## What a Prompt Can Control

A prompt can tell the model:

- what task to perform
- what context to use
- what constraints to respect
- what output format to produce
- what examples define the desired behavior
- what to do when information is missing

It cannot guarantee correctness. Reliability comes from prompts **plus**
appropriate context, tools, validation, and evaluation.

## In-Context Learning

During ordinary inference, the model's weights stay fixed. The model conditions
its next-token predictions on the tokens already present in the context.

For an autoregressive language model:

$$
p_\theta(x_{t+1} \mid x_{1:t})
$$

Changing the prompt changes the context the model conditions on; it does not
perform a gradient update.

This is the basic setting for zero-shot, one-shot, and few-shot prompting.

## Zero-, One-, and Few-Shot Prompting

### Zero-shot

Give the task and constraints without demonstrations.

```text
Classify the support ticket as billing, technical, or account.
Return only the category.

Ticket:
I was charged twice for the same invoice.
```

### One-shot

Add one example, often to demonstrate format.

```text
Classify the ticket.

Example:
Input: I forgot my password.
Output: account

Input: I was charged twice for the same invoice.
Output:
```

### Few-shot

Add several examples when the task has subtle boundaries, unusual labels, or
formatting conventions.

More examples are **not automatically better**. Demonstrations consume context
and can introduce bias, contradictions, or accidental patterns. The right
number and ordering should be tested on representative cases.

## Why Examples Help

Examples can communicate things that are awkward to specify in prose:

- label boundaries
- tone
- output structure
- edge-case behavior
- how much detail is expected

They work best when they are representative and internally consistent.

Avoid inferring a universal mathematical learning curve from the number of
examples. Few-shot performance is task- and model-dependent.

## Structure Before Clever Phrasing

A reliable prompt usually separates four concerns:

```text
Task:
[what to do]

Context:
[the information to use]

Constraints:
[what must or must not happen]

Output:
[the required shape]
```

Clear Markdown headings, XML-like tags, or other delimiters can make boundaries
easier for a model to interpret.

They are **not a security boundary**. Untrusted text inside delimiters can still
contain adversarial instructions, so prompt injection must be addressed with
tool permissions, data-flow controls, validation, and application-level
guardrails.

## Output Contracts

If another system will consume the response, specify the contract explicitly.

```text
Return JSON only.

Schema:
{
  "priority": "low | medium | high",
  "reason": "short string",
  "needs_human_review": true | false
}
```

Then validate the result in code. Do not rely on prompt wording as a substitute
for parsing and validation.

## Decomposition

For complex work, break one vague request into observable stages.

Instead of:

```text
Analyze this incident and fix everything.
```

prefer:

```text
1. Extract confirmed facts from the incident log.
2. List unresolved questions.
3. Identify the smallest plausible root-cause hypotheses.
4. Propose tests that distinguish those hypotheses.
5. Recommend a fix only after the evidence supports one.
```

This makes failures easier to inspect and lets tools or humans validate
intermediate artifacts.

## Reasoning and Explanations

Prompts can ask for a concise rationale, a derivation, a checklist, or a
verification step when those outputs are useful to the user.

Do not assume that a generated explanation is a faithful transcript of a
model's internal reasoning. Treat it as another output to evaluate.

For many tasks, a better pattern is:

```text
Return:
1. the answer
2. the key assumptions
3. the evidence or calculation needed to verify it
```

For arithmetic, code, or data work, external calculation and tests are usually
more reliable than asking for longer prose reasoning.

## Context Quality

More context can help, but irrelevant context can also distract the model.

Prefer context that is:

- necessary for the task
- authoritative
- clearly labeled
- free of duplicated or conflicting instructions
- small enough that important details remain easy to locate

For retrieval workflows, measure whether the correct evidence was retrieved
before blaming the generation prompt.

## Position and Long Context

Models can be sensitive to where information appears in a long prompt, but
there is no universal rule that attention simply decays with token distance.

Important requirements should be easy to find, and long-context behavior should
be tested on the target model and workload.

Standard dense self-attention has quadratic compute and memory cost in sequence
length, although many modern systems use optimizations or different attention
patterns.

## Prompt Development Workflow

1. Define the task and a small evaluation set.
2. Write the simplest prompt that could work.
3. Run it on typical and difficult examples.
4. Classify failures: missing context, ambiguous instruction, format failure,
   factual error, tool failure, or model limitation.
5. Change one thing at a time.
6. Re-run the same examples to detect regressions.
7. Keep the prompt only if the measured result improves.

This is more reliable than repeatedly adding instructions until the prompt looks
impressive.

## Common Failure Modes

### Vague success criteria

```text
Make this better.
```

Better:

```text
Rewrite this for a non-technical audience.
Keep all factual claims.
Use at most 150 words.
```

### Conflicting instructions

A prompt that simultaneously requests "be exhaustive" and "answer in one
sentence" forces the model to guess which constraint matters more.

### Overfitted examples

A few demonstrations can accidentally teach irrelevant wording or ordering.
Vary examples and test held-out cases.

### Unsupported current facts

If the task depends on current prices, product behavior, people, laws, or
versions, retrieve or provide current sources instead of expecting prompt
engineering to repair stale model knowledge.

### Treating format as correctness

Perfect JSON can still contain a wrong answer. Validate both structure and
substance.

## A Reusable Template

```text
Objective:
[what outcome is needed]

Inputs:
[authoritative context]

Constraints:
- [constraint]
- [constraint]

When information is missing:
[state whether to ask, abstain, or make an explicitly labeled assumption]

Output:
[format/schema]

Quality checks:
- [observable requirement]
- [observable requirement]
```

## Key Takeaways

- Prompt engineering is interface design, not incantation.
- Examples are useful when they clarify behavior, but more is not always better.
- Generated explanations are outputs, not guaranteed access to internal
  reasoning.
- Delimiters improve structure but do not solve prompt injection.
- Complex tasks benefit from decomposition and observable checks.
- Evaluate prompts on representative cases and keep regression tests.

## References

- Brown et al. (2020), *Language Models are Few-Shot Learners*:
  https://arxiv.org/abs/2005.14165
- Wei et al. (2022), *Chain-of-Thought Prompting Elicits Reasoning in Large
  Language Models*: https://arxiv.org/abs/2201.11903
- Zhou et al. (2022), *Least-to-Most Prompting Enables Complex Reasoning in
  Large Language Models*: https://arxiv.org/abs/2205.10625
