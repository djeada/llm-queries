# DeepSeek-R1 local-running notes — 2025 snapshot

> **Status:** historical snapshot  
> **Original topic:** first-generation DeepSeek-R1 local deployment  
> **Reviewed:** 2026-09-27

This file is retained as a dated reference rather than current model-selection
advice. DeepSeek-R1 was released with the 671B R1/R1-Zero models and six
distilled checkpoints based on Qwen2.5 and Llama 3.x. The official repository
remains the authoritative source for model names, licenses, and serving
recommendations:

- https://github.com/deepseek-ai/DeepSeek-R1

## Why this moved to snapshots

The old guide mixed durable facts with hardware estimates, model comparisons,
and third-party UI instructions that age quickly. Those should not be presented
as permanent setup guidance.

For current local inference setup, use
[`local_setup_guides/local_models_intro.md`](../../local_setup_guides/local_models_intro.md).

## Original model family

The official DeepSeek-R1 repository describes:

- DeepSeek-R1-Zero and DeepSeek-R1 at 671B total parameters
- distilled Qwen-based checkpoints at 1.5B, 7B, 14B, and 32B
- distilled Llama-based checkpoints at 8B and 70B

The official repository documents vLLM and SGLang examples for distilled
checkpoints. Local runtimes such as Ollama may provide their own packaging and
tags; check the runtime's current model library rather than relying on a static
list in this repository.

## Durable takeaway

For any large local model, choose the runtime and checkpoint separately:

1. Decide the capability and context length you need.
2. Choose a checkpoint that fits memory after quantization and runtime overhead.
3. Confirm the exact model tag in the runtime's current registry.
4. Measure latency and memory on your own machine.
5. Record the runtime version, model identifier, quantization, context length,
   and hardware when publishing results.

That process ages better than a table of "recommended models" tied to one year.
