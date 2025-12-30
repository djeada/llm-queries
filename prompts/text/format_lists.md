# Improving Bullet Lists

This guide provides refined prompt templates and examples to help direct a language model (LLM) toward producing well-structured, easy-to-read bullet lists.

## Expected output

- A single-level bullet list
- Full-sentence bullets with one italicized key term each
- No conversational asides or filler

## Defining List Structure and Style

**Prompt:**

```text
Please format your response as a bullet list. Each bullet should be a complete sentence that flows naturally, never starting with a highlighted term. Introduce one *key term* in italics at its first mention. Use neutral words like “helpful” or “useful” for emphasis, avoiding dramatic adjectives like “critical” or “significant.”
```

**Before (model output without prompt):**

```text
- **consistent indentation**: misaligned list levels confuse readers
```

**After (model output with prompt):**

```text
- Using *consistent indentation* helps readers easily follow nested ideas, while misaligned bullets obscure the hierarchy.
```

**Additional Tip:**

* To enforce a specific symbol, add instructions like “Use ‘–’ (dash) for each bullet” or “Use numbered list” as necessary.

## Eliminating Redundant Commentary

**Prompts:**

```text
Keep each bullet concise and fact-based, without unnecessary filler or casual remarks.
```

```text
Avoid conversational asides—each point should present a concrete recommendation or outcome.
```

**Before:**

```text
- We think it’s really helpful to talk about *single bullet symbol* because it can sometimes make lists look neater.
```

**After:**

```text
- Using a *single bullet symbol* across all items ensures visual consistency and minimizes reader distraction.
```

## Enhancing Reader Comprehension

**Prompt:**

```text
Assume the reader is unfamiliar with list formatting. For each bullet, explain the result of applying versus omitting the practice, and provide a brief real-world example.
```

**Before:**

```text
- *parallel structure*: improves clarity
```

**After:**

```text
- Implementing *parallel structure* (e.g., starting each bullet with a verb) enhances readability, while mixing verbs and nouns can make lists feel disjointed.
```

## Varying Sentence Openings

**Prompt:**

```text
Vary the opening of each sentence by sometimes starting with a scenario, question, or result. Do not begin every bullet with the key term.
```

**Before:**

```text
- *contextual introduction* sets the scene.
- *contextual introduction* guides reader understanding.
```

**After:**

```text
- Providing a *contextual introduction* before listing steps gives the reader necessary background information.
- To improve clarity, start by offering a brief scenario that explains the context before presenting the list items.
```

## Full Prompt

```text
Organize your response as a bullet list. Each bullet should be a full sentence that flows naturally and reads smoothly. Do not begin any bullet with a highlighted term, such as a key concept or technical term. Introduce exactly one *key term* in italics at its first mention within the sentence. Use neutral terms like “helpful,” “useful,” or “beneficial” when emphasizing a point; avoid using overly dramatic adjectives like “critical,” “vital,” or “significant.”

- Keep each bullet concise and fact-based, avoiding filler or casual commentary.
- Avoid conversational asides. Each point should provide a concrete recommendation or result.
- Assume the reader is unfamiliar with list formatting. For each bullet, explain what happens when the practice is applied versus omitted, and provide a brief real-world example if possible.
- Vary sentence openings: do not begin every bullet with the key term. Start with a scenario, question, or result when appropriate.
- Use a consistent symbol for each bullet (either a dash or numbered list) unless otherwise instructed.
```

## Step-by-Step Prompt Development Workflow

1. Describe the topic e.g., best practices for list formatting.
2. Specify whether to use bullets or a numbered list, the requirement for full sentences, the use of italics for key terms, and tone guidelines.
3. Demonstrate one before-and-after bullet, such as *consistent indentation*.
4. Request different sentence openings, and include scenarios that explain the difference between applying and omitting the practice.
5. Review the output, then adjust the prompt to address any gaps or missing details.
