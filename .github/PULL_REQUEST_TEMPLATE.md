## What changed?

Describe the change and why it belongs in this repository.

## Content lifecycle

- [ ] Evergreen
- [ ] Version-sensitive
- [ ] Experimental evaluation
- [ ] Dated / historical snapshot
- [ ] Project / experiment
- [ ] Repository maintenance

If a content file was added, moved, or reclassified, update
`content-registry.json`.

For active version-sensitive content, include a real **Last verified** date in
the document and registry. Do not bump the date without checking the
instructions.

## Validation

- [ ] Ran `python3 scripts/repo_check.py --write-generated` when registry/content paths changed
- [ ] Ran `python3 scripts/repo_check.py`
- [ ] Checked current product/version claims against primary sources
- [ ] Added observable pass criteria for new evaluations
