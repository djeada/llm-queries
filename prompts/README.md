# Prompts library

Reusable prompt templates for concrete tasks. The library favors prompts that
state inputs, constraints, and expected outputs clearly enough to evaluate.

## Categories

| Category | Purpose |
| --- | --- |
| [Blender](blender/) | Small scene-generation and simulation tests |
| [Game development](game_dev/) | Cross-tool asset and playable-game workflows |
| [Job search](job_search/) | Resume and interview tasks |
| [Math](math/) | Mathematical and LaTeX cleanup |
| [Social media](social_media/) | Social copy and captions |
| [Text](text/) | Writing, formatting, simplification, and notes |

For the complete generated file list, use the
[repository catalog](../CATALOG.md).

## Browse by use case

### Writing and editing

- [Improve article](text/improve_article.md)
- [Format lists](text/format_lists.md)
- [Simplify vocabulary](text/simplify_vocabulary.md)
- [Generate notes](text/generate_notes.md)
- [Remove LLM giveaway phrases](text/llm_giveaway_phrases.md)

### Career

- [Resume](job_search/resume.md)
- [Interview questions](job_search/interview_questions.md)

### Technical and math

- [Sanitize LaTeX](math/sanitize_latex.md)

### Social media

- [Instagram](social_media/instagram.md)

### Blender and simulation

- [Fluid physics tests](blender/fluid_physics.md)

### Game development

- [Blender → Godot tiny RPG workflow](game_dev/blender_godot_tiny_rpg.md)

## Prompt design rules

A prompt should make the task testable rather than just sound detailed.

Prefer to include:

- the task and intended user
- required input
- constraints and exclusions
- expected output format
- examples when they clarify ambiguity
- a review checklist for subjective work

Avoid:

- claims that a prompt is universally "best"
- hardcoded model compatibility tables that become stale
- unnecessary references to current model names
- vague instructions such as "make it better" without evaluation criteria

## Model compatibility

Prompts are model-agnostic by default.

If a prompt genuinely depends on a specific model, API, tool, or product
behavior, document that dependency in the file and record when it was actually
verified. Do not maintain a global list of "compatible" model families: those
lists age faster than the prompt content itself.

See the [content lifecycle](../docs/content-lifecycle.md) for freshness rules.

## Prompt template

```markdown
# Prompt name

Brief description of what this prompt does and when to use it.

## Best for

- Use case 1
- Use case 2

## Required input

- Required source material or context
- Optional style, audience, length, or formatting constraints

## Expected output

- Output format
- Quality criteria
- Accuracy requirements, if relevant

## Prompt

\`\`\`text
Your prompt text here...
\`\`\`

## Example

**Input:**

> Example input

**Output:**

> Example output

## Notes

- Limitations
- Variations
- Real model/tool test information, if available
```

## Contributing

When adding or moving a prompt:

```bash
python3 scripts/repo_check.py --write-generated
python3 scripts/repo_check.py
```

Then follow [`CONTRIBUTING.md`](../CONTRIBUTING.md).
