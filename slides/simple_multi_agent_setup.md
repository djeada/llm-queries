# Simple Multi-Agent Setup

Multi-agent systems use multiple specialized LLM-powered agents that collaborate to solve complex tasks. This architecture enables more sophisticated workflows than single-agent approaches by dividing responsibilities and leveraging specialization.

## Why Multi-Agent?

Single agents face limitations as task complexity grows:

| Single Agent | Multi-Agent |
|--------------|-------------|
| One massive prompt | Focused, smaller prompts |
| All skills in one context | Specialized expertise per agent |
| Difficult to debug | Clear responsibility boundaries |
| Context window limits | Distributed context |
| One failure mode | Graceful degradation |

## Core Patterns

### Manager-Worker Pattern

A coordinator agent decomposes tasks and delegates to specialists:

```
                    ┌──────────────────┐
                    │   User Request   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Manager Agent   │
                    │  (Orchestrator)  │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │  Research   │   │    Code     │   │   Review    │
    │   Agent     │   │   Agent     │   │   Agent     │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Manager Agent   │
                    │  (Synthesizes)   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Final Response  │
                    └──────────────────┘
```

**When to use**: Complex tasks requiring different expertise areas

### Pipeline Pattern

Agents process sequentially, each refining the previous output:

```
Input ──► Agent 1 ──► Agent 2 ──► Agent 3 ──► Output
          (Draft)     (Review)    (Polish)
```

**Example: Content Creation Pipeline**

```
Topic ──► Research ──► Draft ──► Edit ──► Format ──► Final
           Agent       Agent     Agent    Agent     Output
```

**When to use**: Workflows with clear sequential stages

### Peer-to-Peer Pattern

Agents hand off directly based on task requirements:

```
┌───────────┐     ┌───────────┐     ┌───────────┐
│  Agent A  │◄───►│  Agent B  │◄───►│  Agent C  │
│ (General) │     │(Technical)│     │ (Creative)│
└───────────┘     └───────────┘     └───────────┘
```

**When to use**: Flexible workflows where routing depends on content

### Debate Pattern

Multiple agents argue positions, then synthesize:

```
       ┌──────────────┐
       │   Question   │
       └──────┬───────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Pro    │ │Con    │ │Neutral│
│Agent  │ │Agent  │ │Agent  │
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └─────────┼─────────┘
              ▼
       ┌──────────────┐
       │   Synthesis  │
       │    Agent     │
       └──────────────┘
```

**When to use**: Complex decisions requiring multiple perspectives

## Implementation Components

### Agent Definition

Each agent needs:

```python
class Agent:
    name: str              # Identifier
    system_prompt: str     # Role and instructions
    tools: list[Tool]      # Available capabilities
    model: str             # Which LLM to use
```

### Communication Protocol

Agents need a standard message format:

```python
@dataclass
class AgentMessage:
    sender: str           # Which agent
    recipient: str        # Target agent or "all"
    content: str          # The message
    message_type: str     # "task", "result", "question", "error"
    metadata: dict        # Additional context
```

### State Management

Track progress across agents:

```python
@dataclass
class WorkflowState:
    task_id: str
    current_agent: str
    history: list[AgentMessage]
    artifacts: dict       # Intermediate results
    status: str           # "in_progress", "complete", "failed"
```

## Example: Code Review System

### Agents

1. **Analyzer Agent**: Reads code, identifies areas of concern
2. **Security Agent**: Checks for security vulnerabilities
3. **Style Agent**: Reviews code style and best practices
4. **Summary Agent**: Synthesizes findings into actionable feedback

### Flow

```
Code Submission
      │
      ▼
┌──────────────┐
│   Analyzer   │──────────┐
│    Agent     │          │
└──────────────┘          │
      │                   │
      ├───────────────────┤
      │                   │
      ▼                   ▼
┌──────────────┐   ┌──────────────┐
│   Security   │   │    Style     │
│    Agent     │   │    Agent     │
└──────────────┘   └──────────────┘
      │                   │
      └─────────┬─────────┘
                │
                ▼
         ┌──────────────┐
         │   Summary    │
         │    Agent     │
         └──────────────┘
                │
                ▼
         Review Report
```

### Implementation Sketch

```python
async def review_code(code: str) -> str:
    # Parallel analysis
    security_task = security_agent.analyze(code)
    style_task = style_agent.analyze(code)
    
    security_findings, style_findings = await asyncio.gather(
        security_task, style_task
    )
    
    # Synthesize
    summary = await summary_agent.synthesize(
        code=code,
        security=security_findings,
        style=style_findings
    )
    
    return summary
```

## Key Considerations

### Agent Boundaries

Define clear responsibilities:

| ✅ Good Boundaries | ❌ Poor Boundaries |
|-------------------|-------------------|
| "You analyze security vulnerabilities" | "You help with code" |
| "You format output as markdown" | "You make things better" |
| "You can only call the search tool" | "Use any tool needed" |

### Error Handling

Agents can fail—plan for it:

```python
async def run_with_fallback(primary_agent, fallback_agent, task):
    try:
        result = await primary_agent.run(task, timeout=30)
        return result
    except (TimeoutError, AgentError) as e:
        log_error(e)
        return await fallback_agent.run(task)
```

### Token Budget Management

Track and limit token usage:

```python
class TokenBudget:
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.used_tokens = 0
    
    def can_proceed(self, estimated_tokens: int) -> bool:
        return self.used_tokens + estimated_tokens <= self.max_tokens
    
    def record_usage(self, tokens: int):
        self.used_tokens += tokens
```

### Observability

Log everything for debugging:

```python
def log_agent_call(agent_name, input_msg, output_msg, tokens, latency):
    logger.info({
        "agent": agent_name,
        "input": input_msg[:100],  # Truncate
        "output": output_msg[:100],
        "tokens": tokens,
        "latency_ms": latency
    })
```

## Common Pitfalls

1. **Overengineering**: Start with single agent, add complexity only when needed
2. **Unclear handoffs**: Define exactly when and how agents transfer work
3. **Infinite loops**: Add maximum iteration limits
4. **Token explosion**: Each agent call adds overhead; monitor total usage
5. **Inconsistent context**: Ensure agents have the context they need

## When NOT to Use Multi-Agent

- Simple tasks that one agent handles well
- Latency-critical applications (each agent adds delay)
- When single-agent with tools suffices
- Limited budget for token usage

## Getting Started Checklist

- [ ] Identify if multi-agent is actually needed
- [ ] Define agent roles with clear boundaries
- [ ] Choose orchestration pattern (manager, pipeline, peer)
- [ ] Implement communication protocol
- [ ] Add comprehensive logging
- [ ] Set up error handling and fallbacks
- [ ] Monitor token usage and latency
- [ ] Test with adversarial inputs