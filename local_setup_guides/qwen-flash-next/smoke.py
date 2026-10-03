import json,time,urllib.request,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parent
for _ in range(720):
    if subprocess.run(['systemctl','--user','is-active','--quiet','qwen-flash.service']).returncode:
        raise RuntimeError('Server stopped; see logs/server.log')
    try:
        with urllib.request.urlopen('http://127.0.0.1:8088/health',timeout=5) as r:
            if r.status==200: break
    except Exception: pass
    time.sleep(5)
else: raise RuntimeError('Server did not become ready within one hour')
req=urllib.request.Request('http://127.0.0.1:8088/v1/chat/completions',data=json.dumps({'model':'qwen3.8-flash-next','messages':[{'role':'user','content':'Reply with the word hello.'}],'max_tokens':32,'chat_template_kwargs':{'enable_thinking':False}}).encode(),headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=900) as r: result=json.load(r)
if not result.get('choices'): raise RuntimeError('No generated answer')
(p/'smoke-result.json').write_text(json.dumps(result,indent=2))
print('Server healthy; inference completed. Open http://127.0.0.1:8088',flush=True)
