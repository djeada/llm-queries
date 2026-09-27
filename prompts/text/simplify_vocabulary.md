# Simplify Vocabulary

Use these prompts to make prose easier to read without applying a global word
blacklist.

A word is not "too advanced" in isolation. Whether it should be simplified
depends on audience, context, precision, and tone.

## Best for

- plain-language editing
- documentation for non-specialists
- reducing unnecessary jargon
- adapting expert writing to a broader audience
- making dense prose more direct while preserving technical accuracy

## Expected output

- clearer wording appropriate for the target audience
- technical terms preserved when they are necessary
- meaning, uncertainty, and factual claims preserved
- optional explanations for terms that should not be replaced

## Required input

- source text
- target audience
- desired reading level or tone
- terms that must remain exact

## Base Prompt

```text
Rewrite the text in clearer, more direct language for the audience below.

Audience: [AUDIENCE]
Target level: [PLAIN LANGUAGE / GENERAL PROFESSIONAL / TECHNICAL BEGINNER /
INTERMEDIATE / OTHER]

Terms that must remain exact:
"""
[OPTIONAL TERMS]
"""

Rules:
1. Preserve meaning, facts, uncertainty, names, numbers, and constraints.
2. Replace unnecessarily formal or abstract wording when a simpler expression
   is equally precise.
3. Keep technical terms when replacing them would reduce accuracy.
4. Define an unfamiliar technical term briefly when the audience may need it.
5. Prefer concrete verbs and nouns over nominalizations and vague abstractions.
6. Do not remove transitions merely because they are formal.
7. Do not invent examples, evidence, or claims.
8. Keep the original structure unless changing it clearly improves readability.

Return only the rewritten text.

Text:
"""
[PASTE TEXT]
"""
```

## Explain Before Rewriting

Use this when the document contains specialist terminology and you do not want
the model to simplify away important distinctions.

```text
Identify vocabulary in the passage that may be difficult for [AUDIENCE].

For each item, classify it as:
- KEEP — precise term that should remain
- DEFINE — keep the term but explain it
- SIMPLIFY — a simpler phrase is equally accurate

Give a short reason and suggested wording.

Do not rewrite the passage yet.

Passage:
"""
[PASTE TEXT]
"""
```

## Technical Documentation Variant

```text
Edit this technical documentation for clarity.

Audience: [AUDIENCE]

Requirements:
- Keep API names, command names, identifiers, protocol terms, and defined domain
  terminology unchanged.
- Simplify surrounding prose.
- Break long sentences when that improves comprehension.
- Replace vague verbs such as "utilize" only when the replacement is equally
  precise.
- Preserve MUST/SHOULD/MAY or other normative language exactly.
- Do not change code blocks.

Documentation:
"""
[PASTE DOCUMENTATION]
"""
```

## Before / After Example

**Before**

```text
The implementation facilitates the utilization of a configurable mechanism for
the optimization of request throughput.
```

**After**

```text
The implementation lets you configure how requests are batched to improve
throughput.
```

The change is useful because it replaces abstract nouns with an explicit action;
it is not based on banning words such as "implementation" or "optimization."

## Review checklist

- Simpler wording did not change the technical meaning.
- Necessary domain terms remain intact.
- The rewrite matches the audience rather than an arbitrary banned-word list.
- Normative or legal wording was not weakened.
- No facts or examples were invented.
