# LLM Skills Prompt Library

Reusable prompts for practical LLM work: debugging prompts, designing context,
evaluating outputs, auditing RAG systems, designing agent tools, and choosing
local models. These are the skills that repeatedly matter when building or using
LLM workflows.

## What Belongs Here

A file belongs in this directory when it helps someone do a concrete LLM task
better. Useful skill prompts should produce decisions, tests, rubrics, or
implementation-ready changes.

Good candidates:

- Improve a weak prompt by diagnosing failure modes.
- Decide what context to include, remove, summarize, or retrieve.
- Evaluate model output against task-specific criteria.
- Debug RAG retrieval and citation quality.
- Design tool schemas and guardrails for agents.
- Select a model for local or API-based work under real constraints.

Poor candidates:

- Generic career advice.
- Vague learning plans without artifacts.
- Motivational coaching.
- Prompts that do not produce a checkable result.

## Prompt Index

| Prompt | Use it to |
| ------ | --------- |
| [prompt_debugging.md](prompt_debugging.md) | Diagnose and rewrite prompts that produce weak, vague, or unreliable outputs |
| [context_engineering.md](context_engineering.md) | Decide what context to include, structure, compress, or retrieve |
| [llm_evaluation.md](llm_evaluation.md) | Build task-specific rubrics, test cases, and regression checks |
| [rag_quality_audit.md](rag_quality_audit.md) | Audit retrieval, grounding, citations, and answer quality in RAG systems |
| [agent_tool_design.md](agent_tool_design.md) | Design tool interfaces, guardrails, and agent execution workflows |
| [local_model_selection.md](local_model_selection.md) | Choose local or API models under real constraints |

## Recommended Workflow

1. Start with `prompt_debugging.md` when the output is bad and the cause is
   unclear.
2. Use `context_engineering.md` when the model lacks enough information or is
   distracted by too much information.
3. Use `llm_evaluation.md` before changing prompts, models, or retrieval logic.
4. Use `rag_quality_audit.md` for knowledge-base, citation, or retrieval
   workflows.
5. Use `agent_tool_design.md` when the model needs tools, state, approvals, or
   multi-step execution.
6. Use `local_model_selection.md` when privacy, cost, offline use, or hardware
   constraints affect model choice.

## Quality Checklist

- The prompt asks for the real task, inputs, constraints, and failure examples.
- The output includes a concrete recommendation or edited artifact.
- The model must separate evidence from assumptions.
- The result can be tested with examples, rubrics, logs, or acceptance criteria.
- The prompt avoids claims about current products unless the user provides
  sources or explicitly asks to verify them.
