#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while systemctl --user is-active --quiet qwen-flash-download.service; do sleep 10; done
RESULT=$(systemctl --user show qwen-flash-download.service -p Result --value)
if [[ "$RESULT" != success ]]; then
 echo "Download failed: $RESULT. See logs/download.log."
 exit 1
fi
systemctl --user start qwen-flash.service
python3 "$BASE/smoke.py"
