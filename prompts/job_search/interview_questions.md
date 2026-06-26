# Interview Questions Study Guide

Use this workflow to turn a job description into a structured interview preparation plan with likely questions, answer outlines, and practice drills.

## Best for

- Preparing for behavioral, technical, product, leadership, or case interviews
- Building a question bank from a specific job description
- Drafting STAR, CAR, or SOAR answer outlines from real experience
- Exporting practice material to a spreadsheet or flashcard tool

## Expected output

- A topic list derived from the job description
- Question sets grouped by interview type and skill area
- Practice answer outlines in STAR, CAR, or another specified format
- Optional CSV-ready output
- Follow-up questions and weak-answer warnings

## Required input

- Target job description
- Candidate background or resume
- Interview stage, if known
- Preferred answer framework
- Target company or industry context, if relevant

## Extract Key Topics from Job Description

```text
Analyze the job description below and identify the interview preparation topics a candidate should expect.

Return:
1. 8-12 topic categories.
2. Why each topic matters for this role.
3. Likely interview type: recruiter screen, hiring manager, technical, behavioral, case, portfolio, or executive.
4. Evidence from the job description that supports each topic.

Job description:
"""
[PASTE JOB DESCRIPTION]
"""
```

## Generate Common Interview Questions

```text
Based on the target role and topic below, generate interview questions that are realistic for this role.

Role: [ROLE TITLE]
Topic: [TOPIC]
Interview stage: [STAGE OR "UNKNOWN"]

Return:
- 10 common questions
- 5 difficult follow-up questions
- 3 questions that test practical judgment
- What a strong answer should demonstrate
- Red flags or weak-answer patterns to avoid

Job description:
"""
[PASTE JOB DESCRIPTION]
"""
```

## Create a Practice Answer Study Guide

```text
Help me create interview answer outlines from my real experience.

Framework: [STAR / CAR / SOAR]
Target role: [ROLE TITLE]

Rules:
1. Use only the experience I provide.
2. Do not invent employers, projects, metrics, tools, or outcomes.
3. If an answer needs a stronger example, mark it as [needs better example].
4. Keep answers concise enough to speak in 60-90 seconds.
5. Include one likely follow-up question for each answer.

Questions:
1. [Question 1]
2. [Question 2]
3. [Question 3]

My background/resume:
"""
[PASTE RESUME OR EXPERIENCE NOTES]
"""
```

## Mock Interview Prompt

```text
Run a mock interview for the role below.

Instructions:
- Ask one question at a time.
- Wait for my answer before giving feedback.
- After each answer, score it from 1-5 for relevance, specificity, structure, and credibility.
- Give one concrete improvement and one sharper follow-up question.
- Keep the interview realistic and role-specific.

Role: [ROLE TITLE]
Job description:
"""
[PASTE JOB DESCRIPTION]
"""
```

## Format and Export to CSV

Structure your CSV with headers to track topics, questions, and answers:

```csv
Topic,Question #,Question Text,Answer Format,Answer Text
Product Strategy,1,"How do you define product-market fit?","STAR","Situation: ..."
Product Strategy,2,"Describe a time you pivoted a product based on user feedback.","STAR","Situation: ..."
Data Analysis,1,"What KPIs do you track to measure success?","STAR","Situation: ..."
...
```

**Columns**:

- `Topic`: The category from Step 1.
- `Question #`: Sequential number per category.
- `Question Text`: Full text of the interview question.
- `Answer Format`: e.g., STAR, CAR.
- `Answer Text`: Your crafted answer.

## Final Prep Checklist

- You have at least one strong story for each major job requirement.
- Each story includes context, action, and outcome.
- Metrics are accurate and easy to explain.
- Technical answers include tradeoffs, not just definitions.
- Behavioral answers focus on your actions, not only team activity.
- You can answer "why this role" and "why this company" directly.
