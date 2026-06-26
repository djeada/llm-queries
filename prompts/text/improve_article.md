# Improving Articles with LLM Prompts

Use these prompts to revise, expand, and polish an existing article without losing the author's meaning. The workflow separates structural review, rewriting, tone refinement, and final quality control so the model does not try to solve every problem in one pass.

## Best for

- Blog posts, essays, documentation, newsletters, and draft articles
- Turning thin notes into clearer prose
- Improving flow, examples, and readability while preserving facts

## Expected output

- A revised version of the input text that is clearer, fuller, and better organized
- Preserved claims, names, dates, and technical details unless explicitly corrected
- No invented facts, statistics, quotes, or citations
- Minimal formatting unless the source already uses headings or lists

## Required input

- Draft article or section to revise
- Intended audience
- Desired tone
- Target length, if any
- Any facts, links, or claims that must remain unchanged

## Full Revision Prompt

```text
Act as a senior editor. Revise the article below so it is clearer, more complete, and more professional while preserving the author's core meaning.

Audience: [AUDIENCE]
Desired tone: [TONE]
Target length: [TARGET LENGTH OR "NO SPECIFIC LIMIT"]

Requirements:
1. Preserve factual claims, names, numbers, dates, and technical details unless they are clearly inconsistent.
2. Do not invent facts, citations, quotes, or examples. If a point needs evidence, mark it as [needs source].
3. Expand thin paragraphs with concrete explanation, examples, or transitions where useful.
4. Remove repetition, filler, vague claims, and awkward phrasing.
5. Keep the structure readable with headings only where they help the reader.
6. Return the revised article first.
7. After the article, include a short "Editorial Notes" section listing the most important changes and any claims that need verification.

Article:
"""
[PASTE ARTICLE]
"""
```

## Focused Rewrite Prompt

```text
Rewrite the following section for clarity and flow. Keep the same meaning, but make the prose more polished and easier to read.

Rules:
- Preserve all facts and constraints.
- Do not add unsupported claims.
- Keep the tone [TONE].
- Keep the length roughly [SHORTER / SAME / LONGER].
- Return only the rewritten section.

Section:
"""
[PASTE SECTION]
"""
```

**Example Before:**

```text
Blockchain technology is transformative. It provides security and transparency.
```

**Example After:**

```text
Blockchain technology offers a new way to record transactions that can’t be altered once written. Each transaction is bundled into a “block” and linked to the previous one, creating a chain. This setup makes it nearly impossible for anyone to tamper with past entries, and everyone in the network can trace and verify each step.
```

*ASCII diagram:*  

```
[Block1] -> [Block2] -> [Block3]
```  

## Tone and Style Prompt

**Prompt:**

```text
Adjust the text to match this style:

- Audience: [AUDIENCE]
- Tone: [TONE]
- Reading level: [READING LEVEL]
- Brand/style notes: [STYLE NOTES]

Keep the meaning unchanged. Remove jargon where possible. When a technical term is necessary, define it briefly in plain language. Return only the revised text.

Text:
"""
[PASTE TEXT]
"""
```

**Example Before:**

```text
Kubernetes orchestrates containerized applications across clusters, offering scalability and self-healing.
```

**Example After:**

```text
Think of Kubernetes like a smart dispatcher for shipping containers—except these containers hold pieces of your app instead of goods. It makes sure each piece runs on a healthy server and automatically restarts any that crash, so your app stays up without you swapping in new parts by hand.
```

## Coherence and Flow Prompt

**Prompt:**

```text
Smooth out transitions between sections by adding linking sentences that explain why one topic follows another. Introduce each heading with a brief lead‑in before diving into details.

Do not rewrite the whole article unless necessary. Return:
1. A list of structural issues.
2. Suggested transition sentences.
3. A revised version of only the affected passages.

Article:
"""
[PASTE ARTICLE]
"""
```

**Example Before:**

```markdown
## Scaling Strategies
Use load balancers.

## Monitoring
Track metrics continuously.
```

**Example After:**

```markdown
## Scaling Strategies
When your app grows, you need to spread incoming traffic so no single server buckles under the load. A load balancer sits in front and distributes requests across multiple machines, keeping performance steady as visitors increase.

## Monitoring
With scaling in place, the next step is to watch how your resources behave. By tracking metrics like CPU use and response times, you can spot hiccups early and adjust capacity before slowdowns affect users.
```

## Review Prompt

```text
Review the article below as an editor. Do not rewrite it yet.

Identify:
1. Unclear or underdeveloped sections.
2. Repeated ideas.
3. Claims that need evidence.
4. Tone inconsistencies.
5. Grammar, punctuation, and formatting issues.

Return a prioritized checklist with specific quotes from the article and recommended fixes.

Article:
"""
[PASTE ARTICLE]
"""
```

## Final Checklist

Use this checklist after applying the prompts:

- Each paragraph has a clear purpose.
- Thin sections have examples, explanation, or supporting detail.
- Repeated points have been merged or removed.
- Factual claims have not been invented or exaggerated.
- Tone is consistent for the intended audience.
- Headings and transitions guide the reader through the argument.
- Sections open with a short introduction before headings.
