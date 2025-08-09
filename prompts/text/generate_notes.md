# Generating Ntes with LLMs

Use this guide to write prompts that produce rich, well-organized notes from an LLM, complete with subsections, diagrams, and clear formatting.

## Base Prompt Structure  

Begin with a clear instruction that sets expectations for layout, tone, and detail.  

```text
Create extensive notes on the following topic [INSERT TOPIC HERE].

Maintain divisions into sections and subsections for coherence.  
Use markdown headers (## for sections, ### for subsections) and proper LaTeX formatting for any mathematical expressions.  
Include ASCII graphics to illustrate key concepts.  
Avoid starting sentences with bold terms followed by a colon; instead weave ideas into natural sentences.  
Emphasize important points through phrasing rather than heavy formatting.  
Use only single-level lists and do not nest or embed lists.  
Write in a friendly, conversational tone and vary sentence length for flow.  
Embed examples or analogies within paragraphs instead of isolating them in bullets.  
If a section begins with a header, start with an introductory paragraph before diving into details.
```

## Enhancements for Scientific Topics  

When your notes cover scientific or mathematical material, append the following to your base prompt:  

```text
Formulas and mathematical rigor are essential.
```

This ensures the model includes step-by-step derivations and correctly formatted equations.

## Enhancements for Programming Topics  

For code-focused notes, extend the base prompt with these lines:  

```text
Provide every command with example output and an interpretation of that output in a list.  
When explaining command options or flags, present them clearly in a table.
```

## Verification Checklist  

After generating the notes, verify they meet your standards by checking for:  

- Grammatically perfect but overly complex sentences that obscure meaning.  
- Uniform sentence structures or repeated phrasing that feel robotic.  
- Invented statistics or unsupported facts that lack proper citation.  
- Missing introductory paragraphs under new headers.  
- Nested lists or unexpected list-within-list formatting.  
