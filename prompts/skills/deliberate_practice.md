# Deliberate Practice Prompt

Use this prompt to generate focused exercises that improve a specific skill through repetition, feedback, and increasing difficulty.

## Best for

- Practicing coding, writing, design, communication, analysis, or interview skills
- Creating drills from real work examples
- Getting structured feedback after each attempt
- Moving from passive learning to active improvement

## Expected output

- Practice exercises by difficulty level
- Clear success criteria
- Feedback rubric
- Common mistakes to watch for
- Follow-up drills based on performance

## Required input

- Skill to practice
- Current level
- Target outcome
- Practice time available
- Examples of previous work, if available

## Prompt

```text
Act as a deliberate practice coach. Create a focused practice session for the skill below.

Skill:
"""
[SKILL]
"""

Current level:
"""
[CURRENT LEVEL OR RECENT EXAMPLE OF WORK]
"""

Target outcome:
"""
[WHAT GOOD PERFORMANCE LOOKS LIKE]
"""

Practice constraints:
- Time available today: [TIME]
- Tools allowed: [TOOLS]
- Difficulty: [BEGINNER / INTERMEDIATE / ADVANCED / MIXED]

Return:
1. A short warm-up task.
2. Three focused drills, each with instructions, time limit, and success criteria.
3. One realistic challenge task.
4. A feedback rubric with scores from 1-5.
5. Common mistakes and how to correct them.
6. A reflection prompt to use after the session.

Rules:
- Make each task observable and assessable.
- Increase difficulty gradually.
- Avoid vague advice like "practice more".
- If I provide an attempt, critique it directly and suggest the next drill.
```

## Feedback Prompt

```text
Review my practice attempt using the rubric below.

Rubric:
"""
[PASTE RUBRIC]
"""

My attempt:
"""
[PASTE WORK]
"""

Return:
1. Scores for each rubric category.
2. The strongest part of the attempt.
3. The most important weakness.
4. A concrete revision or next attempt.
5. One drill that targets the weakness.
```

## Difficulty Adjustment Prompt

```text
Adjust the practice tasks based on my performance.

Performance summary:
"""
[WHAT WENT WELL, WHAT WAS HARD, SCORES, OR FEEDBACK]
"""

Create the next session with the right difficulty. Keep the work challenging but realistic.
```

## Review Checklist

- The exercises target one skill at a time.
- Success criteria are specific.
- Feedback leads to a next action.
- Difficulty increases only when the basics are stable.
