# Local Model Selection

Use this prompt to choose between local models, hosted APIs, or a hybrid setup.
It is designed for practical constraints: hardware, privacy, latency, quality,
cost, offline use, and maintenance effort.

## Best For

- Deciding whether to run a model locally.
- Selecting model size and quantization class for available hardware.
- Comparing local inference against API use.
- Planning private, offline, or low-cost LLM workflows.
- Defining a test before committing to a model.

## Required Input

- Task and quality requirements.
- Hardware: CPU, RAM, GPU, VRAM, storage, OS.
- Privacy, offline, latency, and cost constraints.
- Expected usage volume.
- Candidate models or tools, if already known.

## Prompt

```text
Act as a practical LLM deployment advisor.

Help me choose a model and deployment approach for this task. Prioritize fit to
requirements over benchmark hype.

Task:
"""
[WHAT THE MODEL MUST DO]
"""

Quality requirements:
"""
[ACCURACY, REASONING, CODING, WRITING, MULTILINGUAL, CONTEXT LENGTH, TOOL USE, ETC.]
"""

Hardware and environment:
"""
[CPU, RAM, GPU, VRAM, STORAGE, OS, OLLAMA/LLAMA.CPP/OTHER TOOLS]
"""

Constraints:
- Privacy: [LOW / MEDIUM / HIGH]
- Offline required: [YES/NO]
- Latency target: [TARGET]
- Budget: [BUDGET]
- Expected usage: [REQUESTS PER DAY OR TOKENS]
- Maintenance tolerance: [LOW / MEDIUM / HIGH]

Candidate models or services:
"""
[OPTIONAL SHORTLIST]
"""

Return:
1. Recommended approach: local, API, or hybrid.
2. Model class to test first, including size and quantization guidance.
3. Why this fits the task and constraints.
4. What not to use and why.
5. A small benchmark plan using my real task examples.
6. Deployment risks and mitigations.
7. Questions that require current model documentation or live verification.

Rules:
- Do not claim a model is currently best unless current sources are provided.
- Prefer testing on real examples over relying on generic benchmarks.
- Be explicit about hardware uncertainty.
- Separate must-have requirements from nice-to-have requirements.
```

## Follow-Up: Benchmark Results

```text
Analyze these model benchmark results.

Task examples, outputs, latency, and resource usage:
"""
[PASTE RESULTS]
"""

Constraints:
"""
[QUALITY THRESHOLD, LATENCY TARGET, PRIVACY NEEDS, COST LIMIT]
"""

Return:
1. Which model is best for this specific task.
2. Tradeoffs by quality, speed, cost, and operational complexity.
3. Failure cases each model still has.
4. Recommendation for production, prototype, or rejection.
5. Next test to run before deciding.
```

## Review Checklist

- Recommendation is tied to the task and hardware.
- Current-product claims are marked for verification.
- The benchmark plan uses real user examples.
- The decision includes quality, latency, privacy, and maintenance tradeoffs.
