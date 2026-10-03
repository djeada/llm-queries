# Roadmap

The goal is not to collect every AI note. The goal is to keep a small,
inspectable knowledge base that stays useful as tools and models change.

## Now: maintenance architecture

- [x] Separate prompts, skills, evaluations, setup guides, snapshots, and projects
- [x] Add generated navigation instead of hand-maintained global indexes
- [x] Validate internal links in CI
- [x] Track content lifecycle and freshness explicitly
- [x] Replace stale local-model recommendation tables with reproducible selection guidance
- [x] Add structured result recording for evaluations
- [x] Add a small evaluation runner for text/JSON test cases
- [x] Add project-level smoke tests where runnable projects exist

## Next: evaluation-first content

Prioritize content that produces observable, repeatable results:

- coding-agent repository tasks
- tool-selection and tool-use tests
- structured-output/schema adherence
- retrieval and citation quality
- multimodal document/image tasks
- MCP application workflows
- local-model latency and memory comparisons

New evaluation suites should define fixtures, pass criteria, and result formats,
not just prompt lists.

## Then: current guides

Maintain a deliberately small set of current guides:

- local inference runtimes
- coding-agent integrations
- context and tool configuration
- evaluation harness setup
- RAG/retrieval debugging

Version-specific guides should have a review interval. Old guides should move to
`snapshots/` when they stop being current.

## Content we should avoid accumulating

- static "best models" leaderboards
- unsourced product comparisons
- news without dates
- setup commands with no verification date
- duplicated indexes
- vague prompt collections with no expected behavior
- project code without a README and status

## Definition of healthy

The repository is healthy when:

1. CI passes.
2. `CONTENT_HEALTH.md` has no overdue active version-sensitive content.
3. New files are present in `content-registry.json`.
4. Evaluations define observable pass criteria and executable cases where practical.
5. Current setup guides were verified recently.
6. Historical material is visibly labeled and linked to a source.
7. Active teaching material avoids undocumented product internals and unsupported formulas.
