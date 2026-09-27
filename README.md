# llm-queries

[![License](https://img.shields.io/github/license/djeada/llm-queries?color=2a9d8f)](LICENSE)
[![Content quality](https://github.com/djeada/llm-queries/actions/workflows/content-quality.yml/badge.svg)](https://github.com/djeada/llm-queries/actions/workflows/content-quality.yml)

A maintained knowledge base for prompts, LLM workflow skills, evaluations,
current setup guides, dated references, teaching material, and small
experiments.

The repository is designed around one constraint: **AI tooling ages quickly**.
Current instructions, evergreen concepts, experimental evaluations, and
historical snapshots are therefore tracked differently instead of being mixed
into one undifferentiated Markdown collection.

## Start here

| Goal | Start here |
| --- | --- |
| Reuse a prompt | [Prompts](prompts/README.md) |
| Debug or design an LLM workflow | [Skills](skills/README.md) |
| Run a repeatable capability test | [Evaluations](evaluations/README.md) |
| Run models or coding agents locally | [Local setup guides](local_setup_guides/README.md) |
| Browse all content | [Content catalog](CATALOG.md) |
| See what needs maintenance | [Content health](CONTENT_HEALTH.md) |
| Understand the repo design | [Architecture](docs/architecture.md) |
| See what is next | [Roadmap](ROADMAP.md) |

## Architecture

The repository has distinct content layers:

| Area | Responsibility | Lifecycle |
| --- | --- | --- |
| `prompts/` | Reusable task instructions | Mostly evergreen |
| `skills/` | Reusable LLM workflow procedures | Evergreen or explicitly version-sensitive |
| `evaluations/` | Observable capability tests and benchmark suites | Experimental / version-sensitive |
| `local_setup_guides/` | Commands intended to work now | Active / version-sensitive |
| `projects/` | Self-contained runnable experiments | Project-specific |
| `resources/` | Summaries of external source material | Dated/source-specific |
| `course_reviews/` | Course notes and reviews | Historical |
| `news/` | Notes on specific developments | Historical |
| `slides/` | Teaching material | Evergreen or historical |
| `snapshots/` | Superseded version-specific guidance kept for reference | Historical |

Every non-index content document is registered in
[`content-registry.json`](content-registry.json). The registry records its
kind, freshness class, maintenance status, review interval, and verification
date where relevant.

From that registry, the repository generates:

- [`CATALOG.md`](CATALOG.md) — what exists
- [`CONTENT_HEALTH.md`](CONTENT_HEALTH.md) — what is current, experimental,
  historical, or needs review

See [`docs/architecture.md`](docs/architecture.md) for the full design.

## Maintenance contract

The normal maintenance path is:

```bash
make check
```

It runs repository/content checks, executable-evaluation regression checks, and
the runnable project smoke tests.

The content checker verifies:

- local Markdown links
- registry coverage and metadata validity
- visible lifecycle status for non-active content
- source links for historical material
- minimum prompt structure
- generated catalog and health reports
- verification dates for active version-sensitive guides

After adding, moving, removing, or reclassifying content:

```bash
make generate
make check
```

Pull requests and pushes to `main` run the same structural checks. A scheduled
workflow additionally runs:

```bash
make freshness
```

That means an active version-sensitive guide can become unhealthy simply
because its review date passes. Time is treated as an input to repository
quality.

## Content policy

### Evergreen

Use for concepts and procedures that should survive model churn. Avoid model
names unless they are essential to the concept.

### Version-sensitive

Use for setup instructions, product behavior, APIs, current model/tool
integration, or anything else likely to change.

Active version-sensitive documents must show a real verification date and have
a review interval in the registry.

### Experimental

Use for evaluations that are useful but not yet stable enough to be treated as
a maintained benchmark.

### Historical

Use for course reviews, annual reports, model-release notes, news, and
superseded setup guidance. Historical does not mean useless; it means "do not
mistake this for current operational advice."

## Current local workflows

The old static "best local models" table has been removed. Current guidance is
now process-oriented:

- [Running Models Locally](local_setup_guides/local_models_intro.md)
- [Local Models with Coding Agents](local_setup_guides/local-coding-agents.md)

Both are tracked as version-sensitive and carry real verification dates.

Older DeepSeek-R1-specific local-running notes were moved to
[`snapshots/local-models/deepseek-r1-2025.md`](snapshots/local-models/deepseek-r1-2025.md)
instead of being left in the current setup section.

## Evaluation-first direction

Several files that were previously misclassified as "setup guides" are now
first-class evaluations. The repository also includes a small provider-neutral
JSONL runner, deterministic regression fixture, reproducibility metadata, and a
report comparator.

```bash
make check-evals
```

Future additions should prefer measurable evaluations with fixtures and pass
criteria over unstructured prompt dumps. See [`evaluations/README.md`](evaluations/README.md)
and [`ROADMAP.md`](ROADMAP.md).

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`docs/content-lifecycle.md`](docs/content-lifecycle.md).

A healthy contribution updates the registry when necessary, regenerates derived
files, and passes:

```bash
make check
```

## Reference

- [Content catalog](CATALOG.md)
- [Content health](CONTENT_HEALTH.md)
- [Architecture](docs/architecture.md)
- [Content lifecycle](docs/content-lifecycle.md)
- [Roadmap](ROADMAP.md)
- [Glossary](docs/glossary.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)
