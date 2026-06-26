# Agent Tool Design

Use this prompt when an LLM workflow needs tools, actions, approvals, or
multi-step execution. It helps design clear tool interfaces and guardrails before
implementation.

## Best For

- Designing tool schemas for agents.
- Deciding what should be a tool versus prompt-only behavior.
- Adding approval gates for risky actions.
- Debugging failed tool calls or brittle agent workflows.
- Planning single-agent or multi-agent task decomposition.

## Required Input

- Agent objective.
- Tasks the agent must perform.
- Available tools, APIs, files, or systems.
- Risk level of actions.
- Constraints: permissions, latency, cost, human approval, logging, rollback.

## Prompt

```text
Act as an agent workflow and tool design reviewer.

Design a reliable tool-use workflow for this agent. Focus on clear tool
boundaries, safe execution, observability, and failure handling.

Agent objective:
"""
[WHAT THE AGENT MUST ACCOMPLISH]
"""

Tasks and actions:
"""
[WHAT THE AGENT NEEDS TO READ, DECIDE, CREATE, UPDATE, DELETE, SEND, OR EXECUTE]
"""

Available tools or systems:
"""
[APIS, DATABASES, FILES, BROWSERS, SHELL COMMANDS, TICKETING SYSTEMS, ETC.]
"""

Risks and constraints:
"""
[SECURITY, PRIVACY, COST, LATENCY, DESTRUCTIVE ACTIONS, APPROVALS, COMPLIANCE]
"""

Return:
1. Recommended workflow: single agent, manager-agent, handoff, or non-agentic.
2. Tool inventory with:
   - Tool name
   - Purpose
   - Inputs
   - Outputs
   - Side effects
   - Risk level
   - Approval needed: yes/no
3. Tool schema suggestions with clear parameter names and descriptions.
4. Guardrails and validation checks before tool calls.
5. Failure handling and rollback strategy.
6. Logging fields for debugging and monitoring.
7. Minimal test scenarios for tool behavior.

Rules:
- Do not make something a tool if static context or deterministic code is better.
- Separate read-only tools from state-changing tools.
- Require approval for irreversible, costly, external, or sensitive actions.
- Make tool outputs structured enough for the agent to use reliably.
```

## Follow-Up: Debug Tool Failures

```text
Diagnose these failed agent tool calls.

Agent instructions:
"""
[PASTE INSTRUCTIONS]
"""

Tool definitions:
"""
[PASTE TOOL NAMES, DESCRIPTIONS, PARAMETERS, AND OUTPUTS]
"""

Failure logs:
"""
[PASTE TOOL CALLS, ERRORS, BAD ARGUMENTS, OR BAD RESULTS]
"""

Return:
1. Likely cause of each failure.
2. Prompt changes.
3. Tool schema changes.
4. Validation or guardrail changes.
5. Regression tests to add.
```

## Review Checklist

- Tool responsibilities are narrow and explicit.
- Side effects and approval rules are clear.
- The workflow handles missing data, tool errors, and partial completion.
- Logs are sufficient to debug failures.
