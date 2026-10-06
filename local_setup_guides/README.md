# Local Setup Guides

Current, reproducible setup instructions for local model runtimes and local
coding-agent workflows, plus experimental multimodal asset workflows.

This directory is intentionally narrow. Benchmark suites and MCP tests live in
[`evaluations/`](../evaluations/); old version-specific setup notes live in
[`snapshots/`](../snapshots/).

## Current guides

| Guide | Purpose | Last verified |
| --- | --- | --- |
| [Running Models Locally](local_models_intro.md) | Runtime/model selection, sizing, API use, reproducible benchmarking | 2026-09-27 |
| [Local Models with Coding Agents](local-coding-agents.md) | Ollama `launch` integrations for coding agents | 2026-09-27 |

| [Qwen3.8-Flash-Next](qwen-flash-next.md) | Tested RTX 5060 setup: llama.cpp CUDA, verified downloads, CPU offloading, and systemd services | 2026-10-03 |

## Experimental guides

| Guide | Purpose | Source verification |
| --- | --- | --- |
| [Image-to-3D assets](image-to-3d-assets.md) | TripoSR baseline, optional FLUX/Qwen/Hunyuan/MIA setup, and controlled asset experiments; full GPU pipeline not yet tested | 2026-10-06 |

## What belongs here

A local setup guide should contain commands a reader can run today and should
identify:

- supported operating systems
- runtime/tool versions when material
- exact commands
- verification steps
- reproducibility information
- links to primary documentation
- a real `Last verified` date

If the guide describes an old model release or setup that is no longer the
recommended path, move it to [`snapshots/`](../snapshots/) rather than
silently rewriting the historical document.

## Validation

Repository checks track these guides as version-sensitive content. Active
version-sensitive guides have a review interval in
[`content-registry.json`](../content-registry.json), and the scheduled CI
freshness check will fail once they become overdue.
