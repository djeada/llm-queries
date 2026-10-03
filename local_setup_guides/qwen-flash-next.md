# Qwen3.8-Flash-Next on an 8 GB NVIDIA GPU

> **Freshness:** version-sensitive · **Last verified:** 2026-10-03

Run Qwen3.8-Flash-Next locally with llama.cpp, CPU expert offloading, and disk-backed model loading. This guide records a working RTX 5060 setup and includes the scripts needed to reproduce it on Linux.

## Tested Setup and Results

| Component | Tested configuration |
|-----------|----------------------|
| GPU | NVIDIA GeForce RTX 5060, 8 GB VRAM |
| CPU | Intel Core i7-12700KF, 12 cores / 20 threads |
| System RAM | 32 GB installed, about 31 GiB usable |
| Storage | NVMe SSD, about 650 GB free before installation |
| NVIDIA driver | 590.48.01 |
| Runtime | Official llama.cpp b11371, Ubuntu x86-64 CUDA 12.8 binaries |
| Model | Unsloth Qwen3.8-Flash-Next UD-IQ4_XS, three GGUF shards |
| Download size | 93,682,584,224 bytes, about 93.7 GB / 87.2 GiB |
| Model revision | `38bb39ee97821de2c9009abb7e93950eec396e66` |
| Context / concurrency | 16,384 tokens / one slot |
| Web interface | `http://127.0.0.1:8088` |

All three shards passed SHA256 verification. The server returned `{"status":"ok"}` from `/health` and answered a test request with `hello`.

The short test processed 18 prompt tokens in about 12.26 seconds and reported about **1.47 prompt tokens/s** and **1.41 generated tokens/s**. Only two tokens were generated, so this is a smoke test, not a sustained speed benchmark. The server reported the model loaded about 46 seconds after startup.

The [reference benchmark](https://github.com/lukaLLM/Qwen3.8-Flash-Next-VRAM-Benchmark) reports approximately 35.7 tokens/s for an 8 GiB VRAM tier on a much larger GPU with capped VRAM and about 91 GiB of usable system RAM. That result does not predict the speed of this RTX 5060 with 32 GB RAM. Here, the model is larger than RAM and must rely on SSD paging.

## 1. Check Prerequisites

You need Linux x86-64, a working NVIDIA driver, Python 3, curl, tar, and a systemd user session. Allow at least 100 GB of free SSD space for this quantization and the runtime; extra space leaves room for normal system use.

```bash
nvidia-smi
free -h
lscpu
df -h "$HOME"
python3 --version
curl --version
tar --version
systemctl --user is-system-running
```

The installed driver worked with the CUDA 12.8 runtime. We downloaded the matching CUDA libraries instead of installing the full CUDA toolkit or compiling llama.cpp. Docker, Ollama, and nvcc were not needed.

The commands below assume this repository is cloned at `~/my_repos/llm-queries`. Adjust that source path if your checkout lives elsewhere.

## 2. Create the Installation Directory

Copy the [supporting scripts](qwen-flash-next/) into the runtime directory. Model files and downloaded binaries stay outside Git.

```bash
QWEN_DIR="$HOME/Apps/qwen-flash-next"
mkdir -p "$QWEN_DIR"/{runtime,models,logs}
cp "$HOME/my_repos/llm-queries/local_setup_guides/qwen-flash-next/"* "$QWEN_DIR/"
chmod +x "$QWEN_DIR/start.sh" "$QWEN_DIR/finish-setup.sh"
```

The scripts use their own location to find the installation directory. `model-revision.txt` pins the download revision, and `model-manifest.json` records the expected sizes and SHA256 hashes supplied by Hugging Face's LFS metadata.

## 3. Install the Pinned CUDA Runtime

```bash
QWEN_DIR="$HOME/Apps/qwen-flash-next"
RELEASE_URL="https://github.com/ggml-org/llama.cpp/releases/download/b11371"
curl -fL --retry 3 \
  "$RELEASE_URL/llama-b11371-bin-ubuntu-cuda-12.8-x64.tar.gz" \
  -o "$QWEN_DIR/runtime.tar.gz"
curl -fL --retry 3 \
  "$RELEASE_URL/cudart-llama-b11371-bin-ubuntu-cuda-12.8-x64.tar.gz" \
  -o "$QWEN_DIR/cudart.tar.gz"
tar -xzf "$QWEN_DIR/runtime.tar.gz" -C "$QWEN_DIR/runtime"
tar -xzf "$QWEN_DIR/cudart.tar.gz" -C "$QWEN_DIR/runtime"

LD_LIBRARY_PATH="$QWEN_DIR/runtime/cudart-llama-b11371-bin-ubuntu-cuda-12.8-x64:$QWEN_DIR/runtime/llama-b11371" \
  "$QWEN_DIR/runtime/llama-b11371/llama-server" --list-devices
```

The device check should list `CUDA0: NVIDIA GeForce RTX 5060`. Check `--help` in the same environment if you use another runtime version: loading and lazy-reading flag names can differ between builds.

## 4. Download and Verify the Model

Start the downloader as a background user service:

```bash
QWEN_DIR="$HOME/Apps/qwen-flash-next"
systemd-run --user --unit=qwen-flash-download \
  --property="StandardOutput=append:$QWEN_DIR/logs/download.log" \
  --property="StandardError=append:$QWEN_DIR/logs/download.log" \
  /usr/bin/python3 "$QWEN_DIR/download.py"
```

[download.py](qwen-flash-next/download.py) downloads one shard at a time with curl, resumes `.gguf.part` files, checks size and SHA256, and creates a `.verified` marker after success. Verified shards are skipped when rerunning the script. Keep every shard in the same `models` directory: llama.cpp opens the siblings from the first shard's filename.

```bash
systemctl --user status qwen-flash-download
tail -f "$HOME/Apps/qwen-flash-next/logs/download.log"
```

The completion message is `All model shards verified.` A percentage in curl's output refers to the current shard, not the whole model. At roughly 23–24 MB/s, this download took around an hour plus hashing time.

To stop and resume the existing download service:

```bash
systemctl --user stop qwen-flash-download
systemctl --user reset-failed qwen-flash-download
systemctl --user start qwen-flash-download
```

If the transient unit no longer exists after a reboot, repeat the `systemd-run` command. Do not run two downloaders at once. For a checksum failure, stop the downloader, remove only the affected shard's `.gguf.part` file, and restart; a completed file that fails hashing also needs to be removed before downloading it again.

## 5. Register the Local Server

Create a systemd user service with the same memory limits used in this setup:

```bash
QWEN_DIR="$HOME/Apps/qwen-flash-next"
mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/qwen-flash.service" <<EOF
[Unit]
Description=Qwen3.8 Flash Next local llama.cpp server

[Service]
Type=simple
ExecStart="$QWEN_DIR/start.sh"
WorkingDirectory=$QWEN_DIR
MemoryHigh=20G
MemoryMax=24G
MemorySwapMax=0
Restart=no
StandardOutput=append:$QWEN_DIR/logs/server.log
StandardError=append:$QWEN_DIR/logs/server.log

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
```

`MemoryHigh` applies pressure above 20 GB; `MemoryMax` sets a hard 24 GB limit and `MemorySwapMax=0` disables swap for the service. File-backed model pages can still be evicted and read again from SSD. These limits leave room for the desktop but may reduce performance or terminate the server if it cannot stay within the limit. `Restart=no` avoids repeated failed starts.

### Launch Parameters

[start.sh](qwen-flash-next/start.sh) checks for verified shards, sets the CUDA library path, and launches this configuration:

```bash
llama-server \
  --model Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf \
  --alias qwen3.8-flash-next --host 127.0.0.1 --port 8088 \
  --n-cpu-moe 48 -ot per_layer_token_embd=CPU \
  --load-mode mmap --lazy-mode on --fit on --fit-target 1536 \
  --ctx-size 16384 --ubatch-size 256 --batch-size 512 \
  --threads 12 --threads-batch 20 --parallel 1 --flash-attn on \
  --jinja --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0
```

| Setting | Purpose |
|---------|---------|
| `--n-cpu-moe 48` | Keeps all 48 layers' expert weights on the CPU |
| `-ot per_layer_token_embd=CPU` | Places the large lookup table on the CPU |
| `--load-mode mmap --lazy-mode on` | Maps weights and reads supported table rows on demand from disk |
| `--ctx-size 16384 --parallel 1` | Configures one conversation slot with a 16K context |
| `--ubatch-size 256` | Uses a conservative microbatch for limited VRAM |
| `--threads 12 --threads-batch 20` | Uses the CPU's core count for decode and logical thread count for prompt processing |
| `--host 127.0.0.1` | Binds the web interface and API to localhost |

**GPU fitting limitation:** although `--fit on --fit-target 1536` was supplied, the startup log reported `model_params::tensor_buft_overrides already set by user, abort`. Automatic fitting therefore did not run. The server loaded successfully, but this check did not establish how many layers were on the GPU. CUDA device detection alone is not proof of GPU acceleration.

The [benchmark's updated configuration comments](https://github.com/lukaLLM/Qwen3.8-Flash-Next-VRAM-Benchmark/blob/master/docker/docker-compose.yaml) say the non-expert GPU footprint can exceed 8 GB with `-ngl 999`. We omitted that setting. If tuning GPU placement, use an explicit modest layer count and inspect startup logs and `nvidia-smi` rather than assuming every non-expert layer fits.

## 6. Start Automatically After Download and Test Inference

Register the completion service:

```bash
QWEN_DIR="$HOME/Apps/qwen-flash-next"
cat > "$HOME/.config/systemd/user/qwen-flash-finish.service" <<EOF
[Unit]
Description=Start Qwen after download and test inference

[Service]
Type=oneshot
ExecStart="$QWEN_DIR/finish-setup.sh"
TimeoutStartSec=infinity
StandardOutput=journal
StandardError=journal
EOF
systemctl --user daemon-reload
systemctl --user start --no-block qwen-flash-finish
```

[finish-setup.sh](qwen-flash-next/finish-setup.sh) waits for `qwen-flash-download` to stop, checks its result, starts `qwen-flash`, and runs [smoke.py](qwen-flash-next/smoke.py). The test waits up to an hour for a healthy server, submits a small chat request with thinking disabled, and saves the response and timing data to `smoke-result.json`.

```bash
systemctl --user status qwen-flash-download qwen-flash-finish qwen-flash
journalctl --user -u qwen-flash-finish
cat "$HOME/Apps/qwen-flash-next/smoke-result.json"
curl -fsS http://127.0.0.1:8088/health
```

Once the download and completion services have succeeded, they become inactive. The server should remain active. A successful result file verifies actual inference, not just an open port.

## 7. Use the Web Interface or API

Open **http://localhost:8088** in your browser. The built-in llama.cpp interface needs no separate web UI installation.

For API clients, use base URL `http://127.0.0.1:8088/v1` and model name `qwen3.8-flash-next`. This localhost setup has no API key configured.

```bash
curl -fsS --max-time 900 http://127.0.0.1:8088/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3.8-flash-next",
    "messages": [{"role": "user", "content": "Reply with the word hello."}],
    "max_tokens": 32,
    "chat_template_kwargs": {"enable_thinking": false}
  }'
```

## 8. Manage and Troubleshoot the Server

```bash
systemctl --user stop qwen-flash
systemctl --user start qwen-flash
systemctl --user restart qwen-flash
tail -f "$HOME/Apps/qwen-flash-next/logs/server.log"
```

The server was not enabled at login. To enable it after successful validation:

```bash
systemctl --user enable qwen-flash
# Undo login startup:
systemctl --user disable qwen-flash
```

Background user services survive closing the terminal. Whether they survive logging out depends on the system's user-session and lingering settings; this setup did not change those settings.

| Symptom | Check or next step |
|---------|--------------------|
| Missing verified shard | Check download status and `logs/download.log`; wait for checksum verification |
| Cannot load CUDA libraries | Check the two extracted runtime directories and the library path in `start.sh` |
| GPU allocation failure | Close GPU-heavy applications or try a lower explicit `-ngl` and smaller context |
| Server killed by memory limit | Inspect `systemctl --user status qwen-flash` and `logs/server.log`; try 4K context |
| Very slow responses | Check RAM pressure and SSD activity; 32 GB cannot keep this quant fully resident |
| Browser cannot connect | Check `/health`, server status, and whether port 8088 is already occupied |
| Fitting aborted with tensor overrides | Supply an explicit layer count; the automatic fitter did not support this configuration in the tested run |

For a manual tuning run, first stop the service so only one server uses the model:

```bash
systemctl --user stop qwen-flash
QWEN_CONTEXT=4096 "$HOME/Apps/qwen-flash-next/start.sh" -ngl 12
```

That example is a tuning starting point, not a measured improvement. Manual launches do not inherit the service's RAM limits. Stop the manual process with Ctrl+C before starting the service again. To adjust service parameters, edit `start.sh` in the installation directory and restart the service.

## References

- [llama.cpp b11371 release](https://github.com/ggml-org/llama.cpp/releases/tag/b11371) — pinned runtime and CUDA libraries.
- [Unsloth GGUF model](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) — quantized weights and shard metadata.
- [Qwen model](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) — original checkpoint.
- [VRAM benchmark](https://github.com/lukaLLM/Qwen3.8-Flash-Next-VRAM-Benchmark) — reference performance, offloading experiments, and their hardware limitations.
