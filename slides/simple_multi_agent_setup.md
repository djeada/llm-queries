# Multi-Agent Systems: When and How to Use Them

A multi-agent system coordinates more than one model-powered component or agent.

That can be useful, but it is not automatically more capable, reliable, or
easier to debug than a single agent. Every additional agent adds another model
call, state boundary, permission surface, latency cost, and possible failure.

Start with the simplest architecture that can satisfy the task.

## First Question: Do You Need Multiple Agents?

Before creating roles, compare these options:

```text
deterministic code
      │
single model call
      │
single agent + tools
      │
explicit workflow / state machine
      │
multiple agents
```

Move downward only when the simpler design has a measured limitation.

Multiple agents can be justified when work has genuinely separable contexts,
permissions, ownership, or execution environments.

Examples:

- one component has access to sensitive data another must not see
- independent subtasks can execute in parallel
- one agent is responsible for a durable workflow stage with a clear contract
- specialized tools or sandboxes need different permission boundaries
- independent review is useful and measured to catch failures

"Different expertise personas" alone is weak justification if every role uses
the same model, context, and tools.

## Define Contracts, Not Personas

A useful agent boundary specifies:

```text
responsibility:
inputs:
outputs:
allowed tools:
side effects:
state it owns:
timeout:
retry policy:
approval rules:
failure behavior:
```

Compare:

**Weak**

```text
You are the smart research agent.
```

**Better**

```text
Input: research question + approved source domains.
Output: JSON array of claims with source URLs and quoted evidence locations.
Tools: web search and page retrieval only.
Side effects: none.
Stop when: five supported claims are found or evidence is insufficient.
```

The second component is testable.

## Pattern 1: Manager and Workers

A manager decomposes work and assigns bounded subtasks.

```text
request
   │
manager
   ├────► worker A ───┐
   ├────► worker B ───┼──► manager synthesis
   └────► worker C ───┘
```

Use this when decomposition is dynamic and the manager has enough information to
decide which work is needed.

Risks:

- manager creates redundant or underspecified tasks
- workers receive inconsistent context
- synthesis drops important evidence
- token and latency cost grows quickly
- manager becomes a single point of failure

Evaluate decomposition quality separately from worker quality.

## Pattern 2: Explicit Pipeline

Stages execute in a known sequence.

```text
input -> extract -> verify -> transform -> publish
```

If routing is deterministic, these stages may not need to be autonomous agents
at all. Plain code plus model calls is often easier to operate.

Use agents only where a stage genuinely needs model-driven decisions or tools.

## Pattern 3: Handoff

One agent transfers ownership to another component under explicit conditions.

```text
triage
  ├─ billing -> billing workflow
  ├─ technical -> support workflow
  └─ risky action -> human approval
```

A handoff contract should state:

- trigger
- data transferred
- data withheld
- new permissions
- who owns the next response/action
- what happens if the target rejects the handoff

## Pattern 4: Independent Review

A second component reviews a concrete artifact.

```text
producer -> artifact -> reviewer -> pass / defects
```

This can help when the reviewer has an independent rubric, evidence source, or
tool.

It is less useful when both calls simply repeat the same vague judgment. Correlated
model errors can survive "multiple opinions."

Review should target observable criteria such as tests, citations, schema,
policy, or source evidence.

## State Architecture

Multi-agent failures often come from unclear state ownership.

Separate:

### Task state

```text
task_id
current_stage
status
deadline
requested_output
```

### Evidence / artifacts

```text
source documents
retrieved evidence
code patches
test results
generated files
```

### Execution history

```text
agent/tool
input reference
output reference
start/end time
error
retry count
approval
```

Do not rely on every agent receiving the entire chat transcript as the state
model.

## Tool and Permission Boundaries

Permissions should follow least privilege.

A research component may only need read access. A deployment component may need
write access but should require approval. An email component should not
automatically inherit shell or database permissions.

For every tool, document:

- read-only vs state-changing
- external side effects
- sensitive inputs/outputs
- idempotency
- rollback or compensation
- approval requirement

Multi-agent architecture does not reduce risk if all agents share unrestricted
tools.

## Concurrency

Parallelism is useful only when tasks are independent enough to run
concurrently.

```text
        ┌─ task A ─┐
input ──┼─ task B ─┼─► join
        └─ task C ─┘
```

At the join, define what happens when:

- one task fails
- one task times out
- results conflict
- a result arrives after the workflow moved on
- the same side effect is attempted twice

Concurrency without join semantics creates race conditions, not intelligence.

## Failure and Retry Semantics

A robust workflow distinguishes:

- model failure
- tool failure
- validation failure
- timeout
- permission denial
- insufficient information
- user cancellation

Retries need limits and idempotency rules.

```text
attempt
  │
  ├─ transient failure -> bounded retry
  ├─ invalid output -> repair once / fail
  ├─ risky side effect -> do not repeat blindly
  └─ repeated failure -> escalate / stop
```

Infinite "agent debate" is not a recovery strategy.

## Human Approval

Approval gates belong before actions whose consequences warrant human control.

Examples:

- sending a message externally
- deleting or overwriting data
- spending money
- publishing or deploying
- changing access controls
- taking action under material uncertainty

The approval view should show the proposed action and relevant evidence, not
merely "agent wants permission."

## Observability

Log enough to reconstruct execution without depending on hidden model reasoning.

Useful fields:

```text
run_id
task_id
component
model/runtime
prompt/template version
tool name
validated arguments
artifact/evidence references
latency
token/usage metrics
result status
error category
approval event
```

Be careful not to log secrets or unnecessary personal data.

## Evaluation

Compare the multi-agent design against a simpler baseline.

Measure:

- task success rate
- failure categories
- latency
- model/tool calls
- cost or token use
- approval frequency
- recovery rate
- unsafe/invalid actions
- human correction effort

A multi-agent design earns its complexity only if it improves the metrics that
matter enough to justify its operating cost.

### Component tests

Test contracts independently:

- router chooses correct destination
- worker output satisfies schema
- reviewer catches seeded defects
- tool calls respect permissions
- retries stop at the limit

### End-to-end tests

Include:

- normal task
- ambiguous task
- unavailable tool
- conflicting worker results
- timeout
- partial completion
- rejected approval
- malformed tool output

## Example: Code Change Workflow

A defensible workflow might be:

```text
issue
  │
planner (read-only)
  │ plan
  ▼
implementation agent (repo write + tests)
  │ patch + test results
  ▼
reviewer (read-only diff + tests)
  │ defects / pass
  ▼
human approval
  │
  ▼
PR creation
```

Important properties:

- the planner cannot modify code
- the implementation output is a patch plus observable test results
- the reviewer inspects an artifact, not the implementer's hidden reasoning
- external publication occurs after an approval boundary

The same design may also be implemented as one agent with staged permissions.
Measure both before deciding.

## Common Failure Modes

- splitting one task into agents with no real contract boundary
- copying the entire context into every agent
- letting agents share unrestricted tools
- trusting one model to "review" another without a rubric
- using more agents instead of improving retrieval or deterministic code
- losing provenance when outputs are summarized between stages
- retry loops that duplicate side effects
- no global budget or termination condition

## Decision Checklist

Before adopting multi-agent orchestration:

- [ ] A simpler single-agent or deterministic design was tested.
- [ ] Each agent boundary has explicit inputs and outputs.
- [ ] State ownership is defined.
- [ ] Tool permissions differ for a reason and follow least privilege.
- [ ] Timeouts, retries, and join behavior are specified.
- [ ] Side effects are idempotent or protected.
- [ ] Approval gates exist where needed.
- [ ] Logs can reconstruct the workflow.
- [ ] Component and end-to-end evals exist.
- [ ] The multi-agent design beats the simpler baseline on measured goals.

## Key Takeaway

Multi-agent systems are an orchestration technique, not a capability multiplier
by default.

Use them when explicit boundaries or parallel work provide measurable value,
and make those boundaries testable.
