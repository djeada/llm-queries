# Prompt Engineering Whitepaper

Google (for Kaggle 5-Day Gen AI Intensive), September 2024
Link: [Whitepaper on Prompt Engineering](https://www.kaggle.com/whitepaper-prompt-engineering)

## Introduction & foundations

Prompt engineering is about shaping inputs so models produce the results you actually want. It covers the roles of system and user messages, how context windows work, and how settings like temperature and token limits affect output.

## Basic prompting paradigms

Use zero-, one-, or few-shot examples to guide behavior; one-shot often balances clarity with brevity. System and role prompts set the overall behavior or persona. Adding relevant context keeps answers grounded in the right background or documents.

## Advanced prompting patterns

Step-back prompting asks the model to review or refine its own work. Chain-of-thought encourages clear, step-by-step reasoning. ReAct blends reasoning with actions or tool calls so the model can think and then do.

## Automated prompt engineering

You can generate and tune prompt candidates with simple scripts or even with LLMs themselves. Set up evaluation pipelines that score outputs—such as accuracy on a test set—and pick the best prompts based on metrics.

## Code prompting techniques

Ask the model to explain or document code, translate between languages or paradigms, and debug by supplying tests, traces, or error messages. Clear instructions and concrete inputs lead to better fixes.

## Multimodal prompting

Combine text with images or other inputs when the task benefits from it. Keep formatting simple and describe what’s in the visual clearly so the model can anchor its response.

## Best practices

Provide representative examples that include edge cases. Be explicit about the output you want and any constraints. Prefer direct instructions over rigid rules. Manage tokens thoughtfully and break big tasks into smaller steps. Experiment with phrasing, formats, and parameters—and record what works. Share what you learn in a prompt library with version control. Revisit prompts periodically as models evolve.

## Appendix & endnotes

Includes detailed tables of templates by task, references, and acknowledgements.
