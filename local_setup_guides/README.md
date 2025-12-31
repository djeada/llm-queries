# Local Setup Guides

Step-by-step instructions for running LLMs on your own hardware. These guides cover everything from installation to optimization, helping you deploy models locally for privacy, cost savings, or offline use.

## Why Run Models Locally?

| Benefit | Description |
|---------|-------------|
| **Privacy** | Data never leaves your machine |
| **Cost** | No per-request API charges |
| **Offline** | Works without internet connection |
| **Customization** | Fine-tune and modify freely |
| **Latency** | No network round-trip delays |

## Available Guides

| Guide | What It Covers | Hardware Needed |
|-------|---------------|-----------------|
| [Local Models Intro](local_models_intro.md) | Ollama setup, model selection, hardware requirements | 8GB+ RAM |
| [DeepSeek R1](deepseek_r1.md) | Running DeepSeek reasoning models | 16GB+ RAM |

## Quick Start

### 1. Check Your Hardware

Minimum requirements for different model sizes:

| Model Size | RAM | VRAM (GPU) | Example Models |
|------------|-----|------------|----------------|
| 1-3B | 8GB | 4GB | Phi-2, Qwen-1.5B |
| 7-8B | 16GB | 8GB | Llama 3 8B, Mistral 7B |
| 13-14B | 32GB | 16GB | Llama 2 13B, Qwen 14B |
| 32B+ | 64GB+ | 24GB+ | DeepSeek 32B, Llama 70B |

### 2. Install Ollama

The easiest way to run models locally:

```bash
# Install on Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### 3. Pull and Run a Model

```bash
# Download a model
ollama pull llama3.3

# Start chatting
ollama run llama3.3
```

## Guide Contents

### [Local Models Intro](local_models_intro.md)

Complete guide to getting started with local LLMs:

- **Hardware requirements** — RAM, VRAM, and CPU needs
- **Model comparison** — Strengths and weaknesses of popular models
- **Ollama setup** — Installation, model management, API usage
- **Quantization** — Running larger models on limited hardware
- **SDK integration** — Using models from Python and JavaScript

### [DeepSeek R1](deepseek_r1.md)

Running DeepSeek's reasoning models locally:

- **Model variants** — Original vs. distilled versions
- **Installation** — Step-by-step Ollama setup
- **Web interface** — Optional GUI setup
- **Performance tips** — Getting good results on consumer hardware

## Common Setups

### Minimal Setup (8GB RAM)

Best for basic experimentation:

```bash
ollama pull phi3:mini          # 2.7B, fast
ollama pull qwen2:0.5b         # 0.5B, very fast
```

### Recommended Setup (16GB RAM)

Good balance of capability and performance:

```bash
ollama pull llama3.3:8b        # 8B, excellent all-around
ollama pull mistral:7b         # 7B, strong reasoning
```

### Power User Setup (32GB+ RAM or GPU)

For advanced use cases:

```bash
ollama pull deepseek-r1:14b    # 14B, strong reasoning
ollama pull llama3.3:70b       # 70B, frontier-level (needs more RAM)
```

## Troubleshooting

### Model Won't Load

- Check available RAM: `free -h`
- Try a smaller model or quantized version
- Close other applications to free memory

### Slow Response Times

- Enable GPU acceleration if available
- Use a smaller model
- Reduce context length in requests

### API Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart the service
systemctl restart ollama  # Linux with systemd
```

## Planned Guides

See [todo.md](todo.md) for upcoming content:

- Fine-tuning workflows
- Multi-model setups
- Production deployment
- Embedding models for RAG

## Contributing

Have experience with local LLM setups? See [CONTRIBUTING.md](../CONTRIBUTING.md) to add guides.

Good guides include:
- Exact commands with expected output
- Hardware requirements at the top
- Troubleshooting sections
- Performance benchmarks when relevant
