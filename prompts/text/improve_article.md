# Improving Articles with LLM Prompts

Use these refined prompt templates to guide a large language model in revising, expanding, and polishing an existing article. Each prompt targets a specific aspect—detail, tone, coherence, and final review—so your text reads smoothly and clearly, like advice from a friendly mentor.

## Expected output

- A rewritten version of the input text, expanded and clarified
- One continuous response unless the prompt requests sections
- Minimal formatting, with bold used sparingly

### General Revision

**Prompt:**

```text
Revise the following text by:
1. Expanding each paragraph with concrete examples or explanations.
2. Correcting any factual or grammatical errors.
3. Enhancing clarity with straightforward language.

Write in an approachable, no-frills style—as if you’re an older friend explaining things to someone new. Use **bold** sparingly and include simple ASCII diagrams only when they clarify a concept.
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

### Tone & Style

**Prompt:**

```text
Adjust the text to sound direct and friendly, as if talking to a younger friend. Avoid jargon; when a technical term is necessary, define it in plain language.
```

**Example Before:**

```text
Kubernetes orchestrates containerized applications across clusters, offering scalability and self-healing.
```

**Example After:**

```text
Think of Kubernetes like a smart dispatcher for shipping containers—except these containers hold pieces of your app instead of goods. It makes sure each piece runs on a healthy server and automatically restarts any that crash, so your app stays up without you swapping in new parts by hand.
```

### Coherence & Flow

**Prompt:**

```text
Smooth out transitions between sections by adding linking sentences that explain why one topic follows another. Introduce each heading with a brief lead‑in before diving into details.
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

### Final Checklist

Use this checklist after applying the prompts:

- Each paragraph is richer with examples or explanations.
- All errors—factual or grammatical—are corrected.
- Tone remains warm and straightforward, with minimal bolding.
- Sections open with a short introduction before headings.
