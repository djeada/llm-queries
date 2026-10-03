#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export LD_LIBRARY_PATH="$BASE/runtime/cudart-llama-b11371-bin-ubuntu-cuda-12.8-x64:$BASE/runtime/llama-b11371${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
python3 - "$BASE" <<'CHECK'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1])
for e in json.loads((p/'model-manifest.json').read_text()):
 f=p/'models'/pathlib.Path(e['path']).name
 marker=f.with_suffix('.verified')
 if not f.exists() or f.stat().st_size!=e['size'] or not marker.exists() or marker.read_text().strip()!=e['lfs']['oid']:
  sys.exit('Model download/verification pending. Check qwen-flash-download.service.')
CHECK
exec "$BASE/runtime/llama-b11371/llama-server" \
 --model "$BASE/models/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf" \
 --alias qwen3.8-flash-next --host 127.0.0.1 --port 8088 \
 --n-cpu-moe 48 -ot per_layer_token_embd=CPU \
 --load-mode mmap --lazy-mode on --fit on --fit-target 1536 \
 --ctx-size "${QWEN_CONTEXT:-16384}" --ubatch-size 256 --batch-size 512 \
 --threads 12 --threads-batch 20 --parallel 1 --flash-attn on \
 --jinja --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 "$@"
