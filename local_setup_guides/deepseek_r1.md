# DeepSeek R1

DeepSeek R1 is an open-source reasoning model comparable to OpenAI’s o1, with multiple checkpoints and distilled sizes available for different hardware profiles. Ollama provides a lightweight CLI to serve and interact with these models locally. You’ll install Ollama, pull the DeepSeek R1 models you need, and then launch a chat session either via the terminal or through a simple web UI. Smaller R1 variants (1.5 B, 7 B) can run on CPU-only machines with ~16 GB RAM, while larger ones (32 B+) generally require a dedicated GPU to achieve reasonable latency.

## Prerequisites

- A **Linux** distribution (Debian/Ubuntu, Fedora, etc.) with **Python** installed.
- **curl** (for the installer script) and **tar** for manual unpacking.
- Optional but recommended: **Git** (to clone repositories) and **Docker** (for running a local web UI).

## 1. Install Ollama

### Automatic install
Run the official installer script to grab the latest Linux binary:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
This handles architecture detection, download, and setup.

### Manual install
If you prefer manual steps or need to upgrade:
```bash
# Remove older installation if present
sudo rm -rf /usr/lib/ollama

# Download and extract
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
sudo tar -C /usr -xzf ollama-linux-amd64.tgz
```
Then verify:

```bash
ollama --version
```

## 2. Start the Ollama server

Launch Ollama’s local API endpoint:

```bash
ollama serve
```

By default, this listens on `localhost:11434` and remains active until stopped with `Ctrl+C`.

## 3. Pull and List DeepSeek R1 Models

### List available
```bash
ollama list
```
Shows all locally fetched models and their sizes.

### Pull a model
```bash
ollama pull deepseek-r1:671b
```
This command downloads the 671 B-parameter checkpoint; you can replace `671b` with any tag.

## 4. Run a Chat Session

### Via CLI
Interact directly in your terminal:
```bash
ollama run deepseek-r1:7b
```
You’ll get a REPL-style chat prompt where you type questions and see answers inline.

### Through a Web UI (optional)
For a browser-based interface, many users pair Ollama with [Open WebUI](https://github.com/oobabooga/text-generation-webui) using Docker:
```bash
# Example: run Open WebUI container (assuming Ollama server is running)
docker run --gpus all -p 8080:8080 \
  -v ~/.ollama:/root/.ollama \
  ghcr.io/oobabooga/text-generation-webui:latest
```
Then visit `http://localhost:8080` and select your `deepseek-r1` model.

## 5. Short Summary of R1 Model Variants

DeepSeek has open-sourced several R1 checkpoints and distilled versions to suit different hardware profiles:

- **DeepSeek-R1-Zero**: The foundational RL-only model.
- **DeepSeek-R1**: Full-scale 671 B parameters.
- **Six distilled “dense” models** based on LLaMA and Qwen: **1.5 B**, **7 B**, **8 B**, **14 B**, **32 B**, **70 B**, plus the full **671 B**.

### Suitability for Normal Workstations

- **1.5 B & 7 B**: Feasible on CPU-only setups with ≥16 GB RAM; ~10–30 s response times per token.
- **8 B & 14 B**: Better with a mid-range GPU (e.g., NVIDIA RTX 3060 with 12 GB VRAM).
- **32 B+ & 671 B**: Require high-end GPUs or multi-GPU rigs to avoid excessive latency.
