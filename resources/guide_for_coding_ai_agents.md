# Claude Code Best Practices

Anthropic Engineering Guide
Link: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

## Feedback-driven iteration

Give Claude a concrete target—unit tests, a mock, or an expected output—and iterate. Build in short loops: implement, check against the target, refine. If you’re matching a UI, include screenshots or wireframes so Claude can compare directly.

## Testing and code iteration

Lead with tests. Provide cases that define the behavior and use them to validate changes. For visual work, pair Claude with tools like Puppeteer or simulator MCP servers, or paste screenshots for pixel checks. When you need speed inside a sandbox, use “Safe YOLO mode” (`claude --dangerously-skip-permissions`) only in isolated containers with no network access.

## Codebase exploration and Q\&A

Treat onboarding like a conversation. Ask about logging, API design, data flow, or edge cases in plain language. Claude can search the repo and answer without special prompting.

## Git and GitHub integration

Use Claude to dig through history, craft commits, revert changes, resolve conflicts, and graft patches. On GitHub, have it open PRs, handle review feedback, triage and label issues, and fix CI or linter failures—all driven by natural prompts.

## Jupyter notebook workflows

Read and write `.ipynb` alongside outputs and images. Ask for cleanup, better visuals, or a narrative pass to make notebooks presentation-ready.

## Workflow optimization

Be specific about requirements, edge cases, and patterns to follow. Include images or URLs and allow fetching via an allowlist when needed. Mention exact file paths so Claude targets the right places. Interrupt and course-correct mid-stream. Reset context with `/clear` to stay focused. For multi-step tasks, use Markdown checklists, GitHub issues, or a scratchpad. Pipe logs or CSVs into Claude, or wire up custom slash commands and small bash tools to feed data.

## Headless automation

Run non-interactive tasks with `claude -p`. Stream results in JSON with `--output-format stream-json` for programmatic use. Good fits include issue triage on GitHub events, subjective linting, and CI-driven code reviews.

## Multi-Claude workflows

Pair roles: one instance writes code or tests, another reviews and verifies. Keep multiple checkouts or Git worktrees open in separate terminals for parallel efforts. Build small harnesses that fan out requests, invoke allowed tools, and process JSON streams.

## Acknowledgements and resources

Authored by Boris Cherny with contributions from the Anthropic engineering community. See the Claude docs, API references, GitHub repositories, MCP servers, and community forums for deeper dives.
