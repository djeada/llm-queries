# GPT-4.1 Prompting Guide

OpenAI Cookbook example, Apr 14, 2025
Source: [GPT-4.1 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)

## Agentic workflows

Persist until the task is done, use tools instead of guessing, and plan or reflect between calls when it helps. Define tools with clear names and descriptions in the `tools` field, and move any examples to a separate “Examples” section. You can prompt the model to plan explicitly; even simple planning can lift scores on tasks like SWE-bench. A solid template walks through understanding the issue, investigating, planning, implementing, debugging, testing, verifying, and reflecting, with strong testing requirements baked in.

## Long context

GPT-4.1 can take very long inputs (up to 1M tokens). It’s great for “needle-in-a-haystack” retrieval, but quality can drop when you ask it to juggle many items or complex state over time. Say whether it should use only the provided context or also its internal knowledge; if you want strict grounding, tell it to answer “I don’t know” when context is missing. For huge prompts, repeat key instructions both before and after the context; if you only place them once, put them at the top.

## Chain of thought

Even though it’s not a dedicated reasoning model, GPT-4.1 benefits from step-by-step thinking when asked, at the cost of more tokens and latency. End prompts with a nudge like “First, think carefully step by step,” and layer in planning guidance. When something fails, review where it went wrong, capture the fix as a reusable strategy, and guide the model through analysis, context review, and synthesis. A simple structure is: a short “Reasoning strategy,” the user question and any external context, then a concrete step-by-step plan.

## Instruction following

The model tends to follow directions literally, so spell out tone, format, workflow steps, tool rules, and any off-limits topics. A good workflow starts with high-level response rules, adds targeted behavior sections (like “Sample phrases”), uses ordered steps for processes, and gets debugged by tightening vague or conflicting instructions and adding examples. Watch for pitfalls: rigid or conflicting rules can trigger hallucinations, repeated sample lines may be echoed verbatim, and verbosity creeps in unless you bound it.

## General advice

Use a consistent template: role and objective, instructions, any sub-categories, reasoning steps, output format, and a few examples. Pick delimiters that fit the job—Markdown is usually best; XML is handy for nested structure; JSON is bulky and often less effective for instruction blocks. For repetitive or parallel tasks, explicitly ask for the full final output, test parallel tool calls, and consider turning them off if they cause trouble.

## Appendix: file diffs

GPT-4.1 is strong at generating diffs. The recommended V4A format uses an `apply_patch` tool with context lines, `@@` location markers, and `-`/`+` for removals and additions, without line numbers. An “apply patch” shell snippet wraps the diff so it can be executed cleanly in CI.
