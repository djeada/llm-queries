# Skill Gap Analysis Prompt

Use this prompt to compare current skills against a target role, project, certification, or learning goal. It helps separate urgent gaps from nice-to-have improvements.

## Best for

- Preparing for a job change or promotion
- Planning what to learn before starting a project
- Auditing team skills before assigning work
- Prioritizing learning when time is limited

## Expected output

- A structured gap analysis table
- Priority levels for each skill
- Evidence-based assessment of current ability
- Practical next steps and learning recommendations
- Clear distinction between required and optional skills

## Required input

- Target role, project, or goal
- Current skills and experience
- Time available
- Constraints, such as budget, tools, or deadline
- Optional job description, project brief, or competency framework

## Prompt

```text
Act as a skills assessment coach. Compare my current skills against the target goal below and identify the most important gaps.

Target goal:
"""
[ROLE, PROJECT, CERTIFICATION, OR LEARNING GOAL]
"""

Requirements or context:
"""
[PASTE JOB DESCRIPTION, PROJECT BRIEF, OR EXPECTATIONS]
"""

My current skills and experience:
"""
[LIST SKILLS, PROJECTS, TOOLS, YEARS OF EXPERIENCE, EDUCATION, OR RESUME EXCERPT]
"""

Constraints:
- Time available: [TIME]
- Budget: [BUDGET]
- Preferred learning style: [READING / VIDEO / PROJECTS / MENTORSHIP / MIXED]
- Deadline: [DATE OR "NONE"]

Return:
1. A table with: Skill area | Target level | Current evidence | Gap severity | Priority | Recommended action.
2. The top 5 skills I should focus on first.
3. Skills I can safely postpone.
4. Missing information you need from me to make the assessment more accurate.
5. A short explanation of the reasoning behind the priorities.

Rules:
- Do not assume I have skills that are not listed.
- Do not inflate my level based on vague evidence.
- Mark uncertain assessments as [uncertain].
- Prioritize skills by practical impact on the target goal.
```

## Follow-Up Prompt

```text
Turn the top-priority gaps from the previous analysis into measurable learning objectives.

For each objective, include:
- Outcome
- Success criteria
- Practice task
- Estimated time
- Evidence I can produce
```

## Review Checklist

- The analysis uses evidence from your background, not guesses.
- Priorities match the target goal.
- Gaps are specific enough to act on.
- Recommendations respect your time and constraints.
