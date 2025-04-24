**GPT-4.1 Prompting Guide**  

*OpenAI Cookbook example, Apr 14, 2025*  

**Source:** [GPT-4.1 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)  

### 1. Agentic Workflows  
- **System Prompt Reminders:** Include persistence (don’t yield until task complete), tool-calling (use tools, don’t guess), and optional planning (think and reflect between calls).  
- **Tool Calls:** Define tools via the API `tools` field, with clear names and descriptions; examples belong in a separate `# Examples` section of the system prompt.  
- **Prompted Planning:** Induce explicit planning in the prompt to improve performance (e.g., on SWE-bench, +4% with planning).  
- **Sample Prompt (SWE-bench Verified):** Detailed system prompt with high-level strategy, step-by-step workflow (understand, investigate, plan, implement, debug, test, verify, reflect), plus rigorous testing requirements.  

### 2. Long Context  
- **Context Window:** GPT-4.1 supports up to 1 M tokens; performs well on “needle-in-haystack” tasks but may degrade when retrieving many items or complex stateful reasoning.  
- **Tuning Context Reliance:** Specify whether to use only provided context or allow model’s internal knowledge, with clear instructions (e.g., “only use external context; otherwise say you don’t know”).  
- **Prompt Organization:** For long inputs, place instructions both before and after context; if only once, leading before the context is best.  

### 3. Chain of Thought  
- **Purpose:** Although not a reasoning model, GPT-4.1 can “think step by step” when prompted, aiding complex tasks at the cost of more tokens and latency.  
- **Basic CoT Prompt:** End prompts with “First, think carefully step by step…”, then follow with explicit planning instructions.  
- **Refinement:** Audit failures, codify effective strategies, address misunderstandings, and guide systematic step-by-step reasoning.  
- **Example Structure:** `# Reasoning Strategy` (query analysis, context analysis, synthesis), followed by user question and external context, then step-by-step plan.  

### 4. Instruction Following  
- **Literal Adherence:** GPT-4.1 follows instructions more literally, so specify tone, format, workflow steps, tool usage, and topics to avoid explicitly.  
- **Recommended Workflow:**  
  1. Start with high-level **Response Rules**.  
  2. Add sections for specific behaviors (e.g. `# Sample Phrases`).  
  3. Use ordered lists for workflows.  
  4. Debug by checking conflicting or underspecified instructions, then add examples.  
- **Common Failures:** Overly rigid rules can cause hallucinations; repeated sample phrases may lead to verbatim repetition; extra verbosity if not constrained.  
- **Example Prompt (Customer Service):** System prompt with greeting, tool call rules, prohibited topics, sample phrases (before/after tool), output format, and precise response steps.  

### 5. General Advice  
- **Prompt Structure:** Template sections: Role & Objective, Instructions, Sub-categories, Reasoning Steps, Output Format, Examples.  
- **Delimiters:** Markdown recommended (titles, backticks, lists); XML for nested structure; JSON is verbose and less effective; choose format that stands out and suits content.  
- **Caveats:** For very repetitive or parallel tasks, explicitly instruct full output; test parallel tool calls and consider disabling if problematic.  

### 6. Appendix: File Diffs  
- **Diff Support:** GPT-4.1 has strong diff generation capabilities.  
- **Recommended V4A Diff Format:** `apply_patch` tool: context lines, `@@` markers for location, `-`/`+` for removals/additions, no line numbers.  
- **Apply Patch Example:** Bash snippet using `%%bash apply_patch <<"EOF" ... EOF`.  
