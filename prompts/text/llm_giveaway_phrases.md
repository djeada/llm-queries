# Reduce Formulaic AI-Style Prose

Use these prompts to find repetitive, generic, or overly templated prose and
rewrite it into more specific language.

No word or phrase reliably proves that text was written by an AI. Treat the
patterns in this guide as editing signals, **not authorship detection**.

## Best for

- removing repetitive transitions and boilerplate
- replacing vague corporate language with concrete statements
- reducing canned introductions and conclusions
- cleaning model-generated drafts before publication
- making tone match a specific author or publication

## Expected output

- revised text that preserves meaning and factual claims
- specific explanations instead of generic filler
- a short list of edits when requested
- no claim that the original text was or was not AI-generated

## Required input

- the text to edit
- target audience
- desired tone or a writing sample to match
- phrases or facts that must remain unchanged

## Why Not Use a Phrase Blacklist?

Words such as "however," "critical," "ensure," "key," or "in summary" can be
completely appropriate.

A blacklist creates two problems:

1. it removes useful words regardless of context
2. it encourages false confidence about AI authorship

Instead, look for **patterns**:

- repeated sentence openings
- generic claims with no evidence
- unnecessary summaries of obvious points
- abstract nouns where a concrete action would be clearer
- inflated adjectives that add no information
- canned offers of further help in material that is meant to stand alone
- repeated transition phrases
- conclusions that merely restate the introduction

## Editing Prompt

```text
Edit the text below to reduce formulaic, generic, or overly polished phrasing.

Audience: [AUDIENCE]
Desired tone: [TONE]
Optional writing sample to match:
"""
[STYLE SAMPLE]
"""

Rules:
1. Preserve factual claims, names, dates, numbers, and meaning.
2. Do not remove a word merely because it is common in AI-generated text.
3. Replace vague claims with concrete wording only when the source already
   provides the necessary detail.
4. Remove redundant transitions, canned introductions, repeated summaries, and
   generic closing offers when they do not serve the document.
5. Prefer direct verbs and specific nouns over abstract corporate phrasing.
6. Keep useful technical terms.
7. Do not invent anecdotes, evidence, citations, or personal experience.
8. Do not claim that the original text was written by AI.

Return:
- the revised text
- a short "Edits made" list with the main style changes

Text:
"""
[PASTE TEXT]
"""
```

## Diagnostic Prompt

Use this before rewriting when you want to understand the style problem.

```text
Review the text for formulaic prose.

Do not judge whether it was written by a human or AI.

For each issue, return:
- exact phrase or sentence
- pattern: [GENERIC CLAIM / REPETITIVE TRANSITION / CANNED INTRO /
  REDUNDANT SUMMARY / INFLATED LANGUAGE / META-SCAFFOLDING / OTHER]
- why it weakens this specific passage
- a more concrete alternative, if the source provides enough information

Text:
"""
[PASTE TEXT]
"""
```

## Meta-Scaffolding Cleanup

Chat responses sometimes contain useful conversational scaffolding that becomes
awkward when pasted into an article or report.

Examples include:

- "I hope this helps"
- "Feel free to ask if you have more questions"
- "Here's a breakdown"
- "Let me know if you'd like more detail"

These phrases are not inherently bad. Remove them when the target artifact is
supposed to read as a standalone document.

```text
Convert this chat-style draft into a standalone document.

Remove conversational scaffolding that addresses the user or offers future
assistance. Preserve the substantive content and do not add new claims.

Draft:
"""
[PASTE DRAFT]
"""
```

## Review checklist

- The revision is more specific, not merely shorter.
- Useful transitions were kept when they help logic.
- Technical vocabulary was not simplified blindly.
- Facts and uncertainty were preserved.
- No fake personal experience was introduced.
- The result makes no authorship claim based on style alone.
