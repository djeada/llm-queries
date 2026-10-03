# Content Lifecycle

The repository tracks content lifecycle explicitly because model names,
integration steps, product behavior, and recommendations can become stale much
faster than conceptual material.

Lifecycle metadata lives in
[`content-registry.json`](../content-registry.json). The generated
[`CONTENT_HEALTH.md`](../CONTENT_HEALTH.md) makes maintenance debt visible.

## Freshness classes

### Evergreen

Content whose usefulness is not tied to a current product version, model name,
price, or API shape.

Examples: prompt structure, evaluation methodology, transformer fundamentals.

Evergreen does not mean "never review"; it means normal aging does not make the
document operationally unsafe.

### Version-sensitive

Instructions or advice that depends on current software, model availability,
hardware support, product behavior, APIs, or integrations.

Active version-sensitive content must have:

- a `last_verified` date in the registry
- a positive `review_days` interval
- a visible `**Last verified:** YYYY-MM-DD` note in the document

Scheduled CI runs strict freshness checks and fails once the review date passes.

### Dated

Material intentionally tied to a point in time or a specific source/version.

Examples: news, annual reports, course reviews, model-release notes, and
superseded setup guidance.

Dated content is normally historical rather than "stale." Preserve its original
context and add a newer current document elsewhere if needed.

## Status values

### Active

Maintained content that should be safe to treat as current within its declared
freshness class.

### Experimental

Useful work in progress, especially evaluation suites whose methodology has not
yet stabilized.

### Needs review

Content whose structure may still be useful but whose current accuracy has not
been verified. This is explicit maintenance debt, not an implicit promise.

### Historical

A dated record that should not be interpreted as current operational guidance.

### Archived

Material retained only for provenance or links and not expected to receive
normal maintenance.

## Moving content through the lifecycle

Typical transitions:

```text
experimental evaluation -> active evaluation
active version-sensitive guide -> needs-review -> active
active version-sensitive guide -> historical snapshot
dated source summary -> historical
project-doc -> needs-review -> active or archived
```

Do not "refresh" a document by changing only its date. Verification means
checking commands, links, model identifiers, assumptions, and expected behavior.

## Registry rules

Every non-index Markdown file under the managed content roots must have exactly
one registry entry.

The registry stores:

```json
{
  "kind": "guide",
  "freshness": "version-sensitive",
  "status": "active",
  "review_days": 120,
  "last_verified": "2026-09-27"
}
```

Index READMEs are excluded because they describe directories rather than
individual content artifacts.

## Generated files

Do not hand-edit:

- `CATALOG.md`
- `CONTENT_HEALTH.md`

Regenerate them with:

```bash
python3 scripts/repo_check.py --write-generated
```

Then validate:

```bash
python3 scripts/repo_check.py
```

To test review deadlines explicitly:

```bash
python3 scripts/repo_check.py --strict-freshness
```

## Review rules

- Prefer durable concepts over static "best model" lists.
- Put current product facts in version-sensitive content.
- Link to primary sources for current product/API claims.
- Move superseded operational guidance into `snapshots/`.
- Keep evaluations separate from setup instructions.
- Avoid claiming something is "tested" unless the test conditions are recorded.
- Use the registry and generated catalog instead of adding another manual index.
