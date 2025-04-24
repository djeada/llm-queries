# Local Models
Running large language models locally on a Linux workstation has never been easier: tools like Ollama, llama.cpp and GPT4All let you pull open‐source checkpoints (e.g., Meta’s Llama 2, Mistral 7B or DeepSeek-R1 variants) directly from Hugging Face or community repos, apply 4–8-bit quantization to fit within 8–16 GB of GPU or 32–64 GB of RAM, and launch both CLI and lightweight web‐based chat interfaces—all without sending data to the cloud or needing specialized hardware.

## Distilled vs. Original Models

DeepSeek-R1 is a 671 B-parameter reasoning model that achieves performance on par with proprietary “o1” models. The project open-sources both:
- **DeepSeek-R1-Zero** and **DeepSeek-R1** (the full 671 B-parameter checkpoint), and  
- **Six distilled variants** based on Meta’s Llama and Alibaba’s Qwen architectures, fine-tuned to approximate the original’s reasoning via RL-based distillation.

These distilled models include:  
- **Qwen-based**: 1.5 B (mobile), 7 B (8 GB+ VRAM), 14 B (16 GB+ VRAM), 32 B (24 GB+ VRAM)
- **Llama-based**: 8 B (8 GB+ VRAM), 70 B (2×24 GB+ VRAM)

## Cloud Service vs. Local Deployment

**Cloud (API/Web)**
- **Pros**: instant scale, no hardware capex, ready access to large context windows.  
- **Cons**: can become expensive with heavy usage, dependent on Internet, potential data-privacy concerns.

**Local Deployment**
- **Pros**: fully offline, maximal data privacy, zero per-use fees, deep customization and fine-tuning freedom.  
- **Cons**: upfront hardware and setup effort, limited by your machine’s spec.

## Hardware Requirements

- **Memory (RAM + VRAM)** is the main bottleneck.  
- **Precision / Quantization** (Llama 7 B example):  
  - Full precision (FP32): ~28 GB VRAM  
  - FP16 (half): ~14 GB VRAM 
  - 8-bit quant: ~7 GB   
  - 4-bit quant: ~3.5 GB 

Quantization techniques similarly reduce footprint for other 7 B-class models. On CPU-only rigs, plan for ≥64 GB system RAM when running even 7 B models.

## Free Models in 2025

Below are **all** major open-source models you can run locally in 2025 **for free**—sorted by size—with their key strengths and weaknesses.

| Model               | Params | License            | Mem. Req. (approx.)      | Strengths                                              | Weaknesses                              |
|---------------------|-------:|--------------------|--------------------------|--------------------------------------------------------|-----------------------------------------|
| **Mistral 7B**      | 7 B    | Apache 2.0/free    | ~12 GB (FP16) / 7 GB (8-bit) | State-of-the-art open model; excellent reasoning/math  Lacks official chat fine-tune; smaller ecosystem |
| **Llama 2-7B**      | 7 B    | Community, free    | ~14 GB (FP16) / 7 GB (8-bit) | Strong dialogue performance (R2-Chat); broad community | License restrictions vs. “true” open source |
| **MPT 7B**          | 7 B    | Apache 2.0/free    | ~12 GB (FP16)             | Optimized for code, long-context stories (65 k tokens)  | General-purpose quality slightly below top |
| **Falcon Mamba 7B** | 7 B    | Apache 2.0/free    | ~12 GB (FP16)             | SSLM architecture → low memory cost, strong benchmarks | Brand-new; smaller community, fewer fine-tunes |
| **Qwen2-1.5B**      | 1.5 B  | Apache 2.0/free    | ~3 GB (FP16)              | Mobile-friendly; top open benchmarks vs small peers | Limited context (2 k tokens); fewer chat variants |
| **Vicuna 13B**      | 13 B   | CC-BY-NC-SA, free  | ~26 GB (FP16) / 13 GB (8-bit) | Chat-fine-tuned on ShareGPT, strong ChatGPT mimic | Logical reasoning lags larger models      |
| **GPT-J 6B**        | 6 B    | Apache 2.0/free    | ~12 GB (FP16)             | Mature ecosystem; excellent code generation | Older architecture; outperformed by newer 7 B models |

## Ollama

Ollama is a lightweight, extensible framework that packages, serves, and runs large language models entirely on your local machine, without relying on cloud APIs. It offers a unified CLI and HTTP API, a curated “Modelfile” library of open-source LLMs (Llama 3.x, DeepSeek-R1, Mistral, Phi-4, etc.), built-in quantization support for CPU/GPU efficiency, and first-class Python/JavaScript client libraries—all installable in one step via a shell script.

- Ollama treats each model like a Docker container: weights, tokenizer, and config bundled in a single Modelfile that you pull once and run anywhere.  
- Manage models with simple commands: `ollama pull`, `list`, `show`, `run`, and `serve` (to launch a local HTTP endpoint).  
- Behind the scenes, `ollama serve` spins up a RESTful server on `localhost:11434`, letting you `curl` or integrate via client libraries.  
- While focused on Linux and macOS, Ollama also offers a Windows preview with GPU acceleration and OpenAI-compatible API support.  
- Beyond chat, Ollama includes embedding models and a growing tool-calling framework for functions, APIs, and code execution.  
- Use Ollama in Python or JavaScript apps via the official libraries, mirroring the REST API for seamless integration.

## Installation on Linux

1. **Run the installer script** (auto-detects your architecture and sets up the `ollama` binary):  

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. **Verify installation**:
  
```bash
ollama --version
```

3. **(Optional) Manual install or upgrade** by downloading the tarball and extracting to `/usr/lib/ollama`.

## Managing Models

**List available models** (locally pulled):  

```bash
ollama list
```

**Browse the online library** for all supported Modelfiles (Llama 3.x, DeepSeek-R1, Mistral, Gemma, Phi-4, etc.) at the Ollama site.  

**Pull a model** to your machine:  

```bash
ollama pull llama3.3
```

**Inspect model metadata**:  

```bash
ollama show llama3.3
```

## Running and Serving

**Run interactively** (CLI chat REPL):  

```bash
ollama run llama3.3
```

**Serve as an API**:  

```bash
ollama serve
```

Then from another terminal or program:  

```bash
curl http://localhost:11434/api/chat -d '{
  "model":"llama3.3",
  "messages":[{"role":"user","content":"Hello"}]
}'
```

**Access across your network** by binding to `0.0.0.0` or via a reverse proxy like Nginx.

## Programmatic Integration

**Python SDK**

```python
from ollama import Ollama
client = Ollama()
resp = client.chat(model="llama3.3", messages=[{"role":"user","content":"Hi"}])
print(resp)
```

**JavaScript SDK**
  
```js
import Ollama from "ollama";
const client = new Ollama();
const resp = await client.chat({ model: "llama3.3", messages: [{ role: "user", content: "Hi" }] });
console.log(resp);
``` 
