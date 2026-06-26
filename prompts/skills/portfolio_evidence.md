# Portfolio Evidence Prompt

Use this prompt to turn completed practice, projects, or job experience into credible evidence of skill. It is useful for resumes, portfolios, promotion packets, case studies, and interview preparation.

## Best for

- Documenting proof of a skill
- Writing project case studies
- Preparing resume bullets from real work
- Building performance review evidence
- Explaining learning progress to a manager or mentor

## Expected output

- Evidence mapped to specific skills
- Resume or portfolio-ready wording
- Case study outline
- Missing proof or verification notes
- Clear separation between completed work and future plans

## Required input

- Skill or competency to demonstrate
- Completed work, project, or practice artifact
- Role and contribution
- Tools, constraints, and outcomes
- Metrics or qualitative results, if available

## Prompt

```text
Act as a portfolio and career documentation editor. Help me turn the work below into credible evidence of skill.

Skill or competency to demonstrate:
"""
[SKILL]
"""

Completed work:
"""
[DESCRIBE PROJECT, TASK, PRACTICE WORK, OR JOB EXPERIENCE]
"""

My role and contribution:
"""
[WHAT I PERSONALLY DID]
"""

Tools, constraints, and context:
"""
[TOOLS, TEAM SIZE, DEADLINE, LIMITATIONS, AUDIENCE]
"""

Outcomes or evidence:
"""
[METRICS, BEFORE/AFTER, FEEDBACK, LINKS, SCREENSHOTS, TEST RESULTS, DELIVERABLES]
"""

Return:
1. A table mapping evidence to specific skills.
2. Resume bullet options using only verified facts.
3. A portfolio case study outline.
4. Interview talking points.
5. Missing evidence that would make the claim stronger.
6. Claims I should avoid because they are unsupported.

Rules:
- Do not exaggerate ownership, scope, or results.
- Do not invent metrics.
- Use [needs evidence] where proof is missing.
- Keep language professional and specific.
```

## Case Study Prompt

```text
Write a portfolio case study from the verified evidence below.

Audience: [HIRING MANAGER / CLIENT / MANAGER / TECHNICAL REVIEWER]
Tone: clear, professional, specific
Length: [SHORT / MEDIUM / LONG]

Structure:
1. Problem
2. Context and constraints
3. My role
4. Approach
5. Result
6. What I learned
7. Evidence or artifacts

Verified evidence:
"""
[PASTE VERIFIED EVIDENCE]
"""
```

## Review Checklist

- Claims are backed by concrete work.
- Your personal contribution is clear.
- Metrics are accurate or marked as missing.
- The wording is specific enough for interviews.
- The portfolio story explains decisions and tradeoffs, not just outcomes.
