## I. Ollama

**Install & verify**

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama -v
systemctl status ollama
```

**Remove**

```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
sudo rm "$(which ollama)"
sudo userdel ollama
sudo groupdel ollama
sudo rm -rf /usr/share/ollama
```

## II. Qwen (via Ollama)

**Install & verify**

```bash
ollama pull qwen2.5-coder
ollama list
ollama run qwen2.5-coder
```

**Remove**

```bash
ollama rm qwen2.5-coder
```

## III. Claude Code (with Ollama backend)

**Install & verify**

```bash
npm install -g @anthropic-ai/claude-code
which claude

export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434

claude --model qwen2.5-coder
```

**Remove**

```bash
npm uninstall -g @anthropic-ai/claude-code
```

## IV. Aider

**Setup**

```bash
mkdir -p test && cd test
virtualenv venv
source venv/bin/activate
pip install aider-chat
export PATH="$HOME/.local/bin:$PATH"
```

**Run**

```bash
aider --model ollama/qwen2.5-coder
```
