# Local Models with Coding Agents

> **Freshness:** version-sensitive · **Last verified:** 2026-09-27  
> Requires a recent Ollama release; `ollama launch` was introduced in Ollama
> v0.15+.

Ollama's `launch` command configures supported coding tools to use local or
Ollama-hosted models without manually wiring environment variables.

Current Ollama documentation lists integrations including Claude Code,
OpenCode, Codex, and Droid:

- https://ollama.com/blog/launch

## 1. Install or update Ollama

Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

Official download page:

- https://ollama.com/download

## 2. Launch a coding agent

Interactive model selection:

```bash
ollama launch claude
```

Other integrations:

```bash
ollama launch opencode
ollama launch codex
```

To configure an integration without launching it immediately:

```bash
ollama launch opencode --config
```

## 3. Pin the model when testing

For reproducible evaluation, select a specific model rather than accepting
whatever default happens to be current:

```bash
ollama launch claude --model <model:tag>
```

Before comparing two models, record:

- Ollama version
- coding-agent version
- exact model tag
- context length
- repository commit
- task prompt
- allowed tools / permissions
- wall-clock time and outcome

## 4. Context length matters

Coding agents often need much more context than one-shot chat. Ollama's launch
documentation recommends a large context window for coding workflows.

If a local model becomes slow or runs out of memory, reduce the context length
or choose a smaller checkpoint. Do not compare two models with materially
different context settings without recording that difference.

## 5. Keep permissions explicit

A coding agent is more than a model. Results depend on what it is allowed to
read, execute, edit, and access over the network.

For evaluations, document the permission boundary:

```text
filesystem: read / write?
shell: enabled?
network: enabled?
git: enabled?
browser: enabled?
approval gates: enabled?
```

A model that was allowed to execute tests is not directly comparable with one
that only generated text.

## 6. Evaluate with repository tasks

Use concrete, checkable work rather than "write a good function":

- fix a failing test
- implement an issue with acceptance criteria
- perform a refactor while preserving tests
- locate and explain a regression
- update documentation and links
- make a small feature and open a PR

Keep those task suites under [`evaluations/`](../evaluations/).

## Maintenance rule

Do not add long-lived environment-variable hacks or hardcoded provider
compatibility claims here. Prefer the integration's current official setup path,
and archive old workflows when the product changes.
