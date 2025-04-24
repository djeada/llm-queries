**Prompt Engineering Whitepaper**  

*Google (for Kaggle 5‑Day Gen AI Intensive), September 2024*  

**Link:** [Whitepaper on Prompt Engineering](https://www.kaggle.com/whitepaper-prompt-engineering)  

### 1. Introduction & Foundations  
- Explains why prompt engineering matters: iteratively shaping inputs to align model outputs with desired results.  
- Defines core prompt elements: system vs. user messages, context windows, temperature, and token limits.  

### 2. Basic Prompting Paradigms  
- **Zero-, One-, and Few-Shot:** Trade-offs of examples count; one-shot balances guidance with brevity.  
- **System Prompts & Role Prompts:** Setting behavior and persona (e.g., “You are a helpful assistant”).  
- **Contextual Prompting:** Providing relevant background or documents to ground responses.  

### 3. Advanced Prompting Patterns  
- **Step‑Back Prompting:** Asking model to critique or revise its own output.  
- **Chain of Thought (CoT):** Encourage step-by-step reasoning with explicit instruction (e.g., “First, think through…”).  
- **ReAct (Reason+Act):** Interleave reasoning with external tool calls or actions.  

### 4. Automated Prompt Engineering  
- **Prompt Generation & Tuning:** Use simple scripts or LLMs themselves to generate candidate prompts.  
- **Evaluation Pipelines:** Automate metric-driven selection (e.g., accuracy on test set) to refine prompts.

### 5. Code Prompting Techniques  
- **Explaining Code:** Ask model to annotate or document code snippets.  
- **Translating Code:** Convert between languages or paradigms.  
- **Debugging & Reviewing:** Provide tests or error messages, instruct model to find and fix bugs.  

### 6. Multimodal Prompting  
- Incorporating images or other modalities in prompts.  
- Practical tips for formatting and embedding visual data.  

### 7. Best Practices Summary  
- **Provide Representative Examples:** Few-shot examples should cover edge cases.  
- **Be Explicit & Specific:** Clearly define the desired output format and constraints.  
- **Use Instructions Over Constraints:** Preface tasks with “Do X by following these instructions” rather than hard rules.  
- **Control Token Usage:** Set max tokens; break long tasks into smaller steps.  
- **Experiment Rigorously:** Vary prompt phrasing, formats, and model parameters; document outcomes.  
- **Collaborate & Share:** Maintain prompt libraries and version control.  
- **Adapt to Model Updates:** Periodically revisit prompts when underlying models evolve.  

### 8. Appendix & Endnotes  
- Contains detailed tables (e.g., prompt templates by task), bibliographic references, and acknowledgements.  
