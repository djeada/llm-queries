**Claude Code Best Practices**  

*Anthropic Engineering Guide*  

**Link:** [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)  

### 1. Feedback-Driven Iteration  
- Provide clear targets: unit tests, visual mocks, or expected outputs.  
- Use iterative loops: implement, evaluate vs. target, refine 2–3 times for best results.  
- Screenshot-driven cycles: supply tools or paste images so Claude can compare UI mocks directly.  

### 2. Testing & Code Iteration  
- **Test‑First Approach:** Supply test cases to guide implementation and validation.  
- **Screenshot Workflows:** Integrate Puppeteer or simulator MCP servers, or paste screenshots for visual matching.  
- **Safe YOLO Mode:** Use `claude --dangerously-skip-permissions` inside isolated containers to run unchecked but guard via containers and no internet.  

### 3. Codebase Exploration & Q&A  
- Onboard to new repositories by asking natural-language questions (e.g., logging flow, API design, edge cases).  
- Claude agentically searches code to answer detailed queries without special prompts.  

### 4. Git & GitHub Integration  
- **Git Commands:** Search history, write commit messages, revert, resolve conflicts, graft patches.  
- **GitHub Ops:** Create PRs, fix review comments, triage issues, categorize open tickets, and address CI/linter failures via natural prompts.  

### 5. Jupyter Notebook Workflows  
- Read/write `.ipynb` files side‑by‑side; Claude interprets outputs (including charts/images).  
- Ask for aesthetic improvements or restructuring to make notebooks presentation‑ready.  

### 6. Workflow Optimization  
- **Be Specific:** Detailed prompts reduce iterations (e.g., specify edge cases, patterns to follow).  
- **Include Images or URLs:** Paste mocks, diagrams, or resource links; allow URL fetching via allowlists.  
- **Mention Files Explicitly:** Use tab‑completion for file paths to target precise resources.  
- **Course Correction:** Interrupt streams, revise prompts, and leverage escape shortcuts to steer direction.  
- **Context Management:** Use `/clear` to reset irrelevant history; maintain focus.  
- **Checklists & Scratchpads:** Employ Markdown checklists or GitHub issues for multi‑step or exhaustive tasks.  
- **Data Injection:** Pipe logs or CSVs into Claude, or use custom slash commands and bash tools to fetch data.  

### 7. Headless Mode Automation  
- Invoke `claude -p` for non-interactive CI hooks, build scripts, or automation pipelines.  
- Stream JSON output (`--output-format stream-json`) for programmatic consumption.  
- **Use Cases:** Issue triage on GitHub events, subjective linting and code reviews integrated into CI.  

### 8. Multi‑Claude Workflows  
- **Writer/Reviewer Pair:** Run parallel Claude instances—one generates code/tests, another reviews or verifies.  
- **Multiple Checkouts & Worktrees:** Open separate repository copies or worktrees in distinct terminals for concurrent tasks.  
- **Custom Harnesses:** Script fan‑out or pipelined loops, calling Claude programmatically with allowed tools and handling JSON streams.  

### 9. Acknowledgements & Resources  
- Author: Boris Cherny; contributions from Anthropic engineering community.  
- **Related Links:** Claude docs, API reference, GitHub repos, MCP server implementations, community forums.  
