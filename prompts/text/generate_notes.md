# Generating Notes with LLMs

Use these prompts to turn source material into structured notes that are detailed enough to study from, but organized enough to scan quickly.

## Best for

- Lecture notes, study guides, book chapters, papers, tutorials, and documentation
- Converting transcripts or long articles into reusable notes
- Building outlines before writing an article or presentation

## Expected output

- A markdown document with clear `##` and `###` sections
- Short introductory paragraph under each main section
- Definitions, examples, and key takeaways
- Tables or ASCII diagrams where they improve understanding
- No unsupported facts beyond the provided source unless explicitly requested

## Required input

- Topic or source text
- Audience level
- Desired depth
- Whether the model may add external knowledge
- Any formatting constraints

## Source-Based Notes Prompt

Use this when you want notes grounded only in the material you provide.

```text
Create detailed study notes from the source material below.

Audience level: [BEGINNER / INTERMEDIATE / ADVANCED]
Depth: [QUICK SUMMARY / STANDARD NOTES / DEEP STUDY GUIDE]

Rules:
1. Use only the supplied source material. Do not add outside facts.
2. Use markdown with `##` for main sections and `###` for subsections.
3. Begin each main section with a short explanatory paragraph.
4. Include definitions for important terms.
5. Use concise bullet lists for details, but avoid nested lists.
6. Add tables or ASCII diagrams only when they clarify relationships.
7. Mark unclear or missing source details as [unclear from source].
8. End with "Key Takeaways" and "Questions to Review".

Source material:
"""
[PASTE SOURCE MATERIAL]
"""
```

## Topic-Based Notes Prompt

Use this when you want the model to create notes from general knowledge. For current, legal, medical, or financial topics, provide sources or verify the result separately.

```text
Create professional study notes on this topic:
[TOPIC]

Audience level: [BEGINNER / INTERMEDIATE / ADVANCED]
Purpose: [EXAM PREP / PRESENTATION / PROJECT REFERENCE / GENERAL LEARNING]

Requirements:
- Organize the notes with `##` and `###` headings.
- Explain concepts in plain language before adding technical detail.
- Include examples after important concepts.
- Use tables for comparisons.
- Use LaTeX for formulas when needed.
- Include common mistakes or misconceptions.
- End with a compact review checklist.
```

## Enhancements for Scientific Topics

When your notes cover scientific or mathematical material, append the following to your base prompt:  

```text
Include formulas, assumptions, units, and step-by-step derivations where relevant. Define every variable the first time it appears. Do not skip algebraic steps that a student would need to understand the result.
```

This ensures the model includes step-by-step derivations and correctly formatted equations.

## Enhancements for Programming Topics  

For code-focused notes, extend the base prompt with these lines:  

```text
For programming topics, include runnable examples, expected output, and a short explanation of what each example demonstrates. Present command flags, configuration options, or API parameters in tables.
```

## Verification Checklist  

After generating the notes, verify they meet your standards by checking for:  

- The notes distinguish source-backed information from added context.
- Important terms are defined before they are used heavily.
- Sections have a readable progression from basics to details.
- Examples actually illustrate the concept being discussed.
- Tables and diagrams clarify rather than decorate.
- No invented statistics, citations, or unsupported claims appear.
