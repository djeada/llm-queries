# Designing Effective Bullet Lists  
Here are several refined prompt templates and concrete examples to guide an LLM toward producing well-structured, natural-reading bullet lists.

## Defining List Structure and Style  

**Prompt:**  

```text
Organize your response as a bullet list. Each bullet must be a full sentence that reads smoothly, never beginning with a highlighted term. Introduce exactly one *key term* in italics at its first mention within the sentence. Avoid dramatic adjectives like “critical” or “significant”; use neutral words such as “helpful” or “useful” when emphasis is needed.
```

**Before (model without prompt):**  

```text
- **consistent indentation**: misaligned list levels confuse readers
```

**After (model with prompt):**  

```text
- When applying *consistent indentation*, readers can follow nested ideas more easily, whereas misaligned bullets often obscure hierarchy.
```

**Additional Tip:**  

- To enforce a specific symbol, add “Use ‘–’ (dash) for each bullet” or “Use numbered list” as needed.

## Eliminating Redundant Commentary

**Prompts:**  

```text
Keep each bullet focused on fact-based details without any filler or casual chatter.
```

```text
Do not include conversational asides—each point should state a concrete recommendation or outcome.
```

**Before:**  

```text
- We think it’s really helpful to talk about *single bullet symbol* because it can sometimes make lists look neater.
```

**After:**  

```text
- Enforcing a *single bullet symbol* across all items ensures visual consistency and reduces reader distraction.
```

## Enhancing Reader Comprehension

**Prompt:**  

```text
Assume the reader may be unfamiliar with list formatting. For each bullet, explain what happens when the practice is applied versus omitted, and include a brief real-world example.
```

**Before:**  

```text
- *parallel structure*: improves clarity
```

**After:**  

```text
- Using *parallel structure* in bullets (e.g., all starting with a verb) enhances readability, whereas mixing nouns and verbs can make lists feel disjointed.
```

## Varying Sentence Openings

**Prompt:**  

```text
Vary your sentence openings by sometimes starting with a scenario, question, or result. Do not open every bullet with the key term.
```

**Before:**  

```text
- *contextual introduction* sets the scene.
- *contextual introduction* guides reader understanding.
```

**After:**  

```text
- Before listing steps, a *contextual introduction* provides necessary background that orients the reader.  
- To improve comprehension, models should offer a concise scenario before diving into list items.
```

## Step-by-Step Prompt Development Workflow

1. Briefly describe the topic (e.g., list formatting best practices).  
2. State bullet vs. numbered list, full-sentence requirement, italics rule, and tone constraints.  
3. Show one before/after bullet using a concrete term like *consistent indentation*.  
4. Ask for different sentence openings and include usage vs. omission scenarios.  
5. Test the prompt, inspect output, and tweak any missing details.
