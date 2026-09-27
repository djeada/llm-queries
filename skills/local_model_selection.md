# Local Model Selection

Use this workflow to decide whether a task should run locally, through a hosted
API, or through a hybrid setup. It deliberately avoids naming a "best" current
model; the output is a shortlist and a benchmark plan tied to the actual task.

## Best for

- deciding whether local inference is worth operating
- choosing a model-size and quantization range for available hardware
- comparing local and hosted inference on the same task
- documenting a reproducible model decision
- avoiding benchmark-driven selection that ignores latency or memory

## Required input

- representative task examples
- minimum acceptable output quality
- CPU, RAM, GPU, VRAM, storage, and OS
- privacy and offline requirements
- latency / throughput target
- expected request or token volume
- budget and maintenance tolerance
- candidate runtimes or models, if already known

## Decision procedure

### 1. Turn requirements into gates

Separate hard requirements from preferences.

Examples of hard gates:

- data must not leave the machine
- must work offline
- p95 latency must stay below a stated threshold
- context must fit a stated workload
- output must satisfy a schema
- model plus runtime must fit available memory

Anything that fails a hard gate is not a candidate, regardless of benchmark
score.

### 2. Define the workload before the model

Create a small evaluation set from real work. A useful starting point is 10–30
examples covering:

- typical requests
- difficult but valid requests
- long-context cases
- malformed or ambiguous input
- cases where abstention is preferable to guessing

Record expected observable behavior rather than hidden reasoning.

### 3. Estimate the hardware envelope

Use parameter count and quantization only as a lower-bound sizing heuristic:

```text
weight_bytes ≈ parameter_count × bits_per_weight / 8
```

Real memory use also includes runtime overhead, KV cache, context length,
architecture-specific buffers, batching, and CPU/GPU offload.

Do not reject or approve a model from parameter count alone. Measure it.

### 4. Build a small candidate set

Shortlist by capability class, not popularity:

- general instruction following
- coding / repository work
- structured output
- long-context synthesis
- multilingual work
- multimodal work
- embeddings / retrieval

For current model names, tags, licenses, context limits, and tool support, verify
the runtime registry and primary model documentation at evaluation time.

### 5. Run the same evaluation for every candidate

Record at least:

```text
model identifier:
runtime + version:
quantization:
context setting:
hardware:
evaluation-set commit:
quality score:
task success rate:
schema / format failure rate:
time to first token:
generation throughput:
peak RAM:
peak VRAM:
errors / retries:
```

Do not compare latency or memory numbers collected under different context,
quantization, or hardware settings as though they were equivalent.

### 6. Decide on the Pareto frontier

A candidate is interesting when another candidate does not clearly beat it on
all dimensions that matter.

Typical tradeoffs:

- quality vs latency
- quality vs memory
- privacy vs operational burden
- API cost vs local hardware cost
- context length vs throughput
- tool reliability vs raw model quality

The final choice should explain which tradeoff is being accepted.

## Prompt

```text
Act as an LLM deployment evaluator.

I need to choose among local inference, a hosted API, or a hybrid setup.

Task:
"""
[WHAT THE SYSTEM MUST DO]
"""

Representative examples:
"""
[PASTE REAL TASK EXAMPLES]
"""

Hard requirements:
"""
[PRIVACY, OFFLINE, QUALITY FLOOR, CONTEXT, LATENCY, FORMAT, ETC.]
"""

Hardware:
"""
[CPU, RAM, GPU, VRAM, STORAGE, OS]
"""

Operating constraints:
- expected volume: [REQUESTS/TOKENS]
- budget: [LIMIT]
- maintenance tolerance: [LOW/MEDIUM/HIGH]
- allowed runtimes/services: [OPTIONAL]

Candidate models/services:
"""
[OPTIONAL SHORTLIST]
"""

Return:
1. Hard requirement gates and how each candidate should be tested against them.
2. A small candidate set or model classes worth testing first.
3. A benchmark plan using the representative examples.
4. Measurements to capture for quality, latency, memory, reliability, and cost.
5. A comparison table template; do not fill unknown values with guesses.
6. Risks, confounders, and current facts that require primary-source verification.
7. A decision rule for choosing among the measured results.

Rules:
- Do not declare a current "best model" from memory.
- Treat parameter-count memory estimates as lower bounds, not guarantees.
- Keep model quality and runtime quality separate.
- Compare candidates under equivalent settings when possible.
- Prefer measured task success over generic leaderboard scores.
```

## Result review

A defensible model-selection result should make it possible for another person
to answer:

- What exact workload was tested?
- What exact model/runtime/configuration was tested?
- Which hard requirements were applied?
- Which outputs counted as success?
- What did latency and memory measurements include?
- Which current facts were verified from primary sources?
- Why was the selected tradeoff acceptable?

If those questions cannot be answered, the model choice is not reproducible.
