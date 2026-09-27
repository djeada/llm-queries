# Running Models Locally

> **Freshness:** version-sensitive · **Last verified:** 2026-09-27  
> Re-check runtime commands and model availability before publishing a benchmark.

This guide focuses on a workflow that survives model churn: install a local
runtime, inspect the model you actually downloaded, size it for your hardware,
and record the configuration used for tests.

The examples use [Ollama](https://ollama.com/) because it provides a small CLI
and local HTTP API. The same selection principles apply to llama.cpp, vLLM,
SGLang, MLX, and other runtimes.

## 1. Install and verify the runtime

Ollama's current Linux installer is:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

Source: https://ollama.com/download/linux

On macOS and Windows, use the current installer from the same download page.

## 2. Choose a model from the live registry

Do not copy a static "best local models" table from this repository. Model
availability, tags, quantizations, context support, and tool support change too
quickly.

Browse the current library at:

- https://ollama.com/search

Then pull one exact tag:

```bash
ollama pull <model:tag>
ollama show <model:tag>
ollama run <model:tag>
```

Record the exact tag in any benchmark or project README.

## 3. Estimate whether it fits

A useful lower-bound estimate for weight storage is:

```text
weight_bytes ≈ parameter_count × bits_per_weight / 8
```

A 7B model at 4 bits is therefore roughly 3.5 GB of weights before metadata,
runtime buffers, KV cache, and other overhead.

Actual memory use depends on more than parameter count:

- quantization format
- context length and KV cache
- architecture and mixture-of-experts activation
- CPU/GPU split and offloading
- batch size
- runtime implementation

Treat any fixed RAM/VRAM table as an estimate, not a guarantee.

## 4. Measure on your machine

Start with a short prompt, then inspect the running model:

```bash
ollama run <model:tag>
ollama ps
```

For repeatable comparisons, record:

```text
runtime version:
model tag:
quantization:
context length:
CPU:
GPU / VRAM:
system RAM:
prompt:
tokens generated:
time to first token:
generation rate:
peak memory:
```

A benchmark without the exact model tag and hardware configuration is hard to
reproduce.

## 5. Use the local API

Ollama exposes a local API. A minimal chat request looks like:

```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "<model:tag>",
    "messages": [
      {"role": "user", "content": "Explain the difference between RAM and VRAM."}
    ]
  }'
```

The runtime must be running locally. Keep the model identifier explicit rather
than depending on an implicit default.

## 6. Pick models by task, not hype

Choose a candidate set based on the workload:

- **coding agent:** tool use, long-context code navigation, patch quality
- **general assistant:** instruction following, latency, memory footprint
- **reasoning:** correctness under a fixed token/time budget
- **multimodal:** supported input modalities and local preprocessing
- **embeddings:** embedding quality, vector dimension, throughput
- **structured output:** schema adherence and retry rate

Use [`evaluations/`](../evaluations/) to create repeatable tests instead of
judging models from one chat transcript.

## 7. Coding-agent integrations

Ollama added `ollama launch` in 2026 for integrations including Claude Code,
OpenCode, and Codex. For current commands and recommended coding models, see:

- https://ollama.com/blog/launch

Keep integration-specific setup in
[`local-coding-agents.md`](local-coding-agents.md), not in this general guide.

## Maintenance rule

This file should explain the process for local inference. Fast-changing model
recommendations belong in dated notes or evaluation results, not in the core
guide.
