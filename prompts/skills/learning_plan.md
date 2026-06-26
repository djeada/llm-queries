# Skill Learning Plan Prompt

Use this prompt to create a realistic roadmap for learning a skill, with milestones, practice tasks, review checkpoints, and evidence of progress.

## Best for

- Self-study plans
- Professional development goals
- Team training paths
- Learning a tool, framework, language, or domain skill

## Expected output

- Week-by-week or phase-based learning plan
- Practice tasks tied to real outcomes
- Resources by type, without unsupported claims
- Checkpoints and assessment criteria
- Final project or proof-of-skill artifact

## Required input

- Skill to learn
- Starting level
- Target level
- Time available per week
- Deadline or desired timeline
- Preferred learning style

## Prompt

```text
Act as a professional learning designer. Create a practical learning plan for the skill below.

Skill:
"""
[SKILL]
"""

Starting level:
"""
[WHAT I ALREADY KNOW]
"""

Target level:
"""
[WHAT I NEED TO BE ABLE TO DO]
"""

Constraints:
- Timeline: [TIMELINE]
- Hours per week: [HOURS]
- Preferred learning style: [READING / VIDEO / PROJECTS / COACHING / MIXED]
- Tools or resources available: [TOOLS]
- Deadline or reason for learning: [CONTEXT]

Return:
1. A brief diagnosis of what matters most for this skill.
2. A phased plan with goals, practice tasks, and deliverables.
3. A weekly schedule if the timeline is 12 weeks or less.
4. A final project that proves practical ability.
5. A review rubric with beginner, intermediate, and strong performance.
6. Risks that could derail the plan and how to adjust.

Rules:
- Prefer hands-on practice over passive consumption.
- Keep the plan realistic for the available hours.
- Do not invent exact course claims or links unless I provide sources.
- If resources are suggested, describe the type of resource to look for.
```

## Example Add-On: Resource Selection

```text
Help me choose learning resources for this plan.

Return a table with:
Resource type | What to look for | Why it helps | Warning signs | How to use it

Do not recommend specific current courses unless you can verify them or I provide a shortlist.
```

## Example Add-On: Short Timeline

```text
Compress this plan into a [NUMBER]-day sprint.

Keep only the highest-impact activities. Include:
- Daily focus
- Practice task
- Expected output
- Review checkpoint
```

## Review Checklist

- Every week or phase produces something observable.
- The plan includes practice, feedback, and review.
- The final project matches the real-world skill target.
- The workload is realistic.
