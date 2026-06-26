# Snake LLM Standalone

This directory is a self-contained copy of the Snake game with the optional local Ollama controller. It does not depend on the personal website repo.

## Requirements

- Node.js 18 or newer
- Python 3, only for the static file server
- Ollama running locally

## Run

From this directory:

```bash
make install-model
make run
```

Open:

```text
http://localhost:8000
```

Stop the background servers:

```bash
make stop
```

## Replace The Model

Use a model only for one run:

```bash
make install-model MODEL=qwen3:4b
make restart MODEL=qwen3:4b
make test MODEL=qwen3:4b
```

Persist a new default model into `.env`:

```bash
make set-model MODEL=qwen3:4b
make install-model
make restart
make test
```

List local Ollama models:

```bash
make models
```

Manual equivalent:

```bash
ollama pull qwen2.5:1.5b
node snake_llm_proxy.js
```

In a second terminal:

```bash
cd projects/snake-llm
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000
```

Start the game, then switch `Controller` to `Local LLM`.

## Test The Proxy Directly

```bash
curl -X POST http://localhost:8787/snake/decide \
  -H 'Content-Type: application/json' \
  --data '{
    "gridSize": 20,
    "head": { "x": 10, "y": 10 },
    "snake": [{ "x": 10, "y": 10 }],
    "direction": "right",
    "food": { "x": 14, "y": 10 },
    "obstacles": [],
    "score": 0,
    "level": 1,
    "legalMoves": ["up", "down", "right"]
  }'
```

Expected shape:

```json
{"move":"right"}
```

## Files

```text
index.html          Standalone page
style.css           Game and control styling
app.js              Snake game plus LLM controller
snake_llm_proxy.js  Local proxy from browser to Ollama
ARCHITECTURE.md     Detailed architecture diagrams
```

## Configuration

The proxy supports:

- `SNAKE_LLM_PORT`, default `8787`
- `OLLAMA_URL`, default `http://localhost:11434/api/chat`
- `SNAKE_LLM_MODEL`, default `qwen2.5:1.5b`
- `SNAKE_LLM_TIMEOUT_MS`, default `8000`
