# A Practical Guide to Building Agents

OpenAI Business Guide (PDF)
Link: [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

## Agent fundamentals

An agent pairs an LLM with tools and clear instructions, executed by a runner through well-described tool interfaces. Keep prompts structured and tools modular so the system is easy to maintain. Think in a loop: perceive, reason, act, and learn from feedback.

## Single-agent architecture

Best for linear tasks with all context in one place. Expose the agent as a tool (`agent.as_tool()`), with clear parameters and expectations. It’s simple to operate, but prompts can get heavy and you’re bounded by the context window.

## Multi-agent patterns

A manager agent can orchestrate work, delegating subtasks to specialists when you need explicit control flow. Alternatively, peers can hand off state directly, shifting ownership as expertise changes for more flexible, distributed workflows.

## Guardrails and safety

Start with privacy and content safety, then layer on edge-case protections over time. Use relevance/safety classifiers, PII filters, and moderation; assign risk levels to tools so higher-risk actions trigger extra checks or human review. Strive for security without sacrificing user experience.

## Human in the loop

Bring people in for high-risk actions, repeated failures, or ambiguous outputs. Common patterns include approval gates, rollbacks, and manual edits—especially for finance, critical systems, or compliance-sensitive work.

## Deployment and monitoring

Track task success, tool usage, latency, and error types. Log decisions and tool calls in a structured way, and alert on failures or policy issues. Iterate continuously: deploy, watch, analyze, then refine prompts, tools, and guardrails.

## Resources and next steps

Use the official SDKs and docs, explore code samples and tutorials, and tap community channels for support and ideas.
 
