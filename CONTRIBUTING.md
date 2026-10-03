# Contributing to llm-queries

The repository is a knowledge library, not a single application. Contributions
should keep content easy to discover, easy to validate, and explicit about how
quickly it can become stale.

## Before you start

Choose the right area:

- `prompts/` — reusable prompt templates
- `skills/` — repeatable LLM workflow playbooks
- `evaluations/` — observable benchmark and tool/MCP test suites
- `local_setup_guides/` — version-sensitive setup instructions
- `resources/` — summaries of external sources
- `course_reviews/` — dated course notes and reviews
- `slides/` — teaching material
- `news/` — dated development notes
- `projects/` — runnable experiments
- `snapshots/` — superseded or intentionally historical guidance

Read [the content lifecycle](docs/content-lifecycle.md) before adding current
model, product, API, or tooling claims.

## Local validation

The repository maintenance scripts use only the Python standard library. Run:

```bash
make check
```

This validates content, executable eval fixtures, and runnable project smoke
tests.

The content checker verifies:

- local Markdown links resolve to files or directories in the repository
- every content file is represented in `content-registry.json`
- registry metadata is valid and active current guides expose matching verification dates
- `CATALOG.md` and `CONTENT_HEALTH.md` match the registry

After adding, moving, deleting, or reclassifying content:

```bash
make generate
make check
```

CI runs the same validation on pull requests and on `main`.

## File names

Use lowercase kebab-case for new files when practical:

```text
good: prompt-debugging.md
good: local-models-intro.md
avoid: My New Prompt.md
```

The repository contains legacy underscore-style names. They do not need to be
renamed solely for style because unnecessary renames break links and history.
When a file is already widely linked, stability is more important than cosmetic
consistency.

## Markdown structure

Use one `#` title per document and a shallow heading hierarchy.

For reusable prompts, prefer:

```markdown
# Prompt name

Brief purpose and when to use it.

## Best for

- Use case

## Required input

- Required context

## Expected output

- What a good response should contain

## Prompt

\`\`\`text
Prompt text...
\`\`\`

## Notes

Limitations, variations, and any real test information.
```

Do not claim a prompt is "tested" unless the model/tool and test date are
recorded.

## Freshness rules

### Evergreen material

Avoid unnecessary product/model names. Prefer concepts, constraints, and
evaluation criteria that survive model churn.

### Version-sensitive material

When adding or materially updating version-sensitive instructions, include a
real verification note near the top:

> **Freshness:** version-sensitive · **Last verified:** YYYY-MM-DD

Only update the date after actually checking the instructions.

### Dated snapshots

Keep dates, versions, and original context visible. Add a newer companion note
instead of rewriting a historical snapshot as if it were current.

## Sources

- Prefer primary documentation for current product/API claims.
- Link factual claims to the source when the claim is not common knowledge.
- Keep summaries original; do not paste long passages from sources.
- Separate your interpretation from what the source explicitly says.

## Projects

A runnable project should be self-contained under `projects/<name>/` and have
its own README with:

- status and purpose
- setup/run instructions
- dependencies
- known limitations
- where LLM/model assumptions enter the design

Do not add repository-root application dependencies for a single project.

## Pull request checklist

Before opening a PR:

- [ ] The file belongs in the chosen directory.
- [ ] Version-sensitive claims have a real verification date when applicable.
- [ ] New facts are sourced appropriately.
- [ ] `make check` passes.
- [ ] `content-registry.json` was updated when content was added, moved, or reclassified.
- [ ] Generated files were refreshed with `make generate`.
- [ ] Historical/source-specific material has a visible status banner and source URL.
- [ ] New executable evals include observable checks rather than hidden-reasoning criteria.
- [ ] The PR explains whether the change is evergreen, version-sensitive, a
      dated snapshot, a project, or repository maintenance.
