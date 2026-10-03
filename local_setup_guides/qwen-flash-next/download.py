#!/usr/bin/env python3
import hashlib,json,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parent
rev=(p/'model-revision.txt').read_text().strip()
for entry in json.loads((p/'model-manifest.json').read_text()):
    name=pathlib.Path(entry['path']).name
    dest=p/'models'/name
    marker=dest.with_suffix('.verified')
    expected=entry['lfs']['oid']
    if dest.exists() and dest.stat().st_size==entry['size'] and marker.exists() and marker.read_text().strip()==expected:
        continue
    partial=dest.with_suffix('.gguf.part')
    if dest.exists(): partial=dest
    url=f"https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF/resolve/{rev}/{entry['path']}"
    print('Downloading',name,entry['size'],flush=True)
    subprocess.run(['curl','-fL','--retry','20','--retry-delay','10','--retry-all-errors','-C','-','-o',str(partial),url],check=True)
    if partial.stat().st_size!=entry['size']: raise RuntimeError('Size mismatch: '+name)
    print('Checking SHA256',name,flush=True)
    h=hashlib.sha256()
    with partial.open('rb') as f:
        for block in iter(lambda:f.read(16*1024*1024),b''): h.update(block)
    if h.hexdigest()!=expected: raise RuntimeError('Checksum mismatch: '+name)
    if partial!=dest: partial.rename(dest)
    marker.write_text(expected+'\n')
print('All model shards verified.',flush=True)
