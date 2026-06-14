# Testing LLM Models on Everyday Tasks

## Purpose

The goal is to evaluate how useful an LLM is for real tasks people perform in work, school, and personal life.

Instead of testing vague categories like “reasoning,” “communication,” or “creativity,” this evaluation focuses on concrete everyday tasks:

* Writing emails
* Summarizing meetings
* Improving essays
* Debugging code
* Planning trips
* Analyzing data
* Drafting complaints
* Explaining concepts
* Completing multi-step work

A strong model should not only answer questions. It should produce outputs that are practical, accurate, polished, and usable with minimal editing.

# 1. Office and Business Tasks

## 1.1 Email Assistant

### Task Types

Use these prompts to test whether the model can handle common workplace communication.

The model should be able to:

* Draft a polite follow-up after no response
* Rewrite an angry or rough message professionally
* Summarize a long email thread
* Respond to a refund or support request
* Write meeting invitations
* Preserve the user’s intended message while improving tone

### Example Test: Professional Client Update

**Prompt:**

> Here is my rough note:
>
> We are late because engineering missed the deadline.
>
> Turn this into a professional client update.

**What this tests:**

* Diplomacy
* Professional tone
* Ability to avoid blame
* Client-facing communication
* Preserving the core message while softening the wording

**A strong model should:**

* Avoid saying “engineering failed”
* Explain the delay clearly
* Sound accountable
* Give the client confidence
* Mention next steps or a revised timeline

### Example Test: Dentist Appointment Email

**Prompt:**

> Write a polite email to cancel my dentist appointment tomorrow because I am sick. Ask if they can reschedule me for next week.

**Rough input version:**

> Hi i cant come dentist tomorow because im sick please cancel it and maybe give me other time next week thanks

**What this tests:**

* Grammar correction
* Politeness
* Email formatting
* Preservation of intent
* Ability to transform informal text into a usable message

**A strong model should produce something like:**

> Subject: Request to Reschedule Appointment
>
> Dear [Dentist Office],
>
> I’m sorry, but I won’t be able to attend my dentist appointment tomorrow because I am feeling unwell. Could you please cancel the appointment and let me know if there are any available times next week to reschedule?
>
> Thank you for your understanding.
>
> Best,
> [Name]

## 1.2 Meeting Assistant

### Task Types

The model should be able to:

* Convert a transcript into structured notes
* Identify decisions
* Extract action items
* Assign owners
* Track deadlines
* Create a follow-up agenda

### Example Test: Meeting Transcript Summarization

**Prompt:**

> Here is a meeting transcript. What decisions were made, what are the action items, and who owns each action item?

**Transcript:**

> Sarah: Thanks everyone for joining. The main topic today is the delay in the mobile app release.
>
> Mike: Right now we're about two weeks behind schedule. The login redesign took longer than expected.
>
> Sarah: Is the redesign finished?
>
> Mike: Mostly. There are still a few bugs on Android.
>
> Priya: QA found three critical issues yesterday. Two are already fixed, but one is still open.
>
> Sarah: Can we still release this month?
>
> Mike: Maybe, but only if the remaining bug is resolved by next Friday.
>
> James: Marketing was planning to launch the campaign on the 25th. If the release slips, we'll need to move that too.
>
> Sarah: Let's avoid committing to a new date today.
>
> Priya: I can have QA retest everything by Wednesday.
>
> Mike: That works. I'll assign someone to focus on the Android issue.
>
> Sarah: Great. Priya will complete retesting by Wednesday, Mike will own the Android bug, and James should prepare a backup launch timeline just in case.
>
> James: Understood.
>
> Sarah: Anything else?
>
> Mike: No, that's everything from engineering.
>
> Sarah: Okay, thanks everyone. Let's meet again next Thursday for an update.

**What this tests:**

* Summarization
* Identifying uncertainty
* Extracting action items
* Assigning owners correctly
* Understanding project risk
* Separating facts from decisions

**A strong model should identify:**

### Key Issue

The mobile app release is about two weeks behind schedule because the login redesign took longer than expected and one critical Android issue remains unresolved.

### Decisions

* The team will not commit to a new release date yet.
* The team will meet again next Thursday for an update.
* Marketing should prepare for the possibility of a delayed campaign.

### Action Items

| Owner | Action Item                               | Deadline                   |
| ----- | ----------------------------------------- | -------------------------- |
| Priya | Complete QA retesting                     | Wednesday                  |
| Mike  | Own and resolve the remaining Android bug | By next Friday             |
| James | Prepare a backup launch timeline          | Before next update meeting |

### Risks

* The release may miss the current month.
* The marketing campaign scheduled for the 25th may need to move.
* The remaining Android bug is the key blocker.

## 1.3 Report Writing

### Task Types

The model should be able to:

* Turn bullet points into polished reports
* Create weekly status updates
* Summarize quarterly results
* Write executive briefings
* Produce concise one-page updates

**Example prompt:**

> Using these notes, write a one-page project update for senior leadership.

**What this tests:**

* Structure
* Professional tone
* Prioritization
* Executive summary writing
* Ability to distinguish important details from background noise

## 1.4 Data Analysis

### Task Types

The model should be able to:

* Identify trends in tables
* Explain why sales dropped
* Find spreadsheet anomalies
* Generate Excel formulas
* Write SQL queries
* Interpret dashboard results

**Example prompt:**

> Here is a table of monthly revenue. What trends stand out?

**What this tests:**

* Quantitative reasoning
* Pattern recognition
* Business interpretation
* Clear explanation
* Ability to avoid overclaiming

# 2. Education and Learning Tasks

## 2.1 Essay Improvement

### Example Test: Weak School Essay Paragraph

**Prompt:**

> Improve this paragraph. Fix grammar, spelling, and style. Strengthen the argument while preserving the original meaning. The result should sound like a competent middle-school or high-school essay, not like a professional academic paper.

**Input paragraph:**

> Climate change is a big problem in the world today and it effects lots of things. The weather is getting hotter because of pollution and people using cars and factories too much. Some people dont think climate change is real but there is many scientists who says it is happening. If we dont do something soon the future could be bad and there might be more floods and droughts. In conclusion climate change is important and everyone should try harder to stop it because it affects the planet and people.

**What this tests:**

* Grammar correction
* Spelling correction
* Fact checking
* Argument strengthening
* Style improvement
* Essay expansion
* Preservation of original meaning
* Ability to match the requested grade level

**A weak model may only fix spelling:**

> Climate change is a big problem in the world today and it affects lots of things...

**A stronger model should improve structure and clarity:**

> Climate change is one of the most serious problems facing the world today. It affects the environment, weather patterns, and people’s lives. Human activities, such as burning fossil fuels in cars and factories, release pollution that traps heat in the atmosphere. Although some people still question whether climate change is real, most scientists agree that it is happening and that human activity is a major cause. If people do not take action, the future could bring more extreme weather, including floods, droughts, and heat waves. For these reasons, climate change is an important issue, and governments, businesses, and individuals should work together to reduce pollution and protect the planet.

**Scoring notes:**

A strong response should sound better than the original but still appropriate for a student. It should not turn the paragraph into an overly advanced academic essay.

## 2.2 Math and Science

### Task Types

The model should be able to:

* Solve algebra problems
* Solve calculus problems
* Explain probability
* Work with linear algebra
* Solve physics problems
* Show derivations
* Check calculations

**Example prompts:**

> A 2 kg block slides down a 30° incline with no friction. Find the acceleration.

> Find the eigenvalues of this matrix.

**What this tests:**

* Accuracy
* Step-by-step reasoning
* Correct formula selection
* Unit handling
* Ability to explain the answer clearly

---

## 2.3 Programming Assignments

### Task Types

The model should be able to:

* Explain algorithms
* Debug homework code
* Generate practice problems
* Implement standard algorithms
* Explain code to a learner

**Example prompt:**

> Implement Dijkstra’s algorithm in Java and explain how it works.

**What this tests:**

* Algorithm knowledge
* Code correctness
* Teaching ability
* Clear explanation
* Appropriate level of detail

# 3. Coding and Software Engineering Tasks

Coding tasks are especially useful for LLM evaluation because many of them can be scored objectively.

## 3.1 Write Functions

### Example Test: Group Emails by Domain

**Prompt:**

> Write a Python function `group_by_domain(emails)` that takes a list of email addresses and returns a dictionary where the keys are domains and the values are lists of emails belonging to that domain.

**Example input:**

```python
[
    "alice@gmail.com",
    "bob@yahoo.com",
    "charlie@gmail.com"
]
```

**Expected output:**

```python
{
    "gmail.com": ["alice@gmail.com", "charlie@gmail.com"],
    "yahoo.com": ["bob@yahoo.com"]
}
```

**Requirements:**

* Ignore invalid email addresses
* Preserve original order
* Time complexity should be O(n)

**What this tests:**

* Requirement following
* Edge cases
* Code quality
* Algorithm design
* Ability to write clean, practical code

**A strong model should consider:**

* Missing `@`
* Empty strings
* Multiple `@` symbols
* Missing local part
* Missing domain
* Preserving the order of valid emails
* Avoiding unnecessary sorting

## 3.2 Debug Errors

### Example Test: Second Largest Unique Number

**Prompt:**

> This function is supposed to return the second largest unique number in a list.

```python
def second_largest(nums):
    nums = sorted(nums)
    return nums[-2]

print(second_largest([5, 1, 7, 7, 3]))
```

> The expected result is `5`, but the function returns `7`.
>
> Explain the bug and provide a corrected implementation.

**What this tests:**

* Bug diagnosis
* Explanation quality
* Correctness of fix
* Understanding of uniqueness
* Handling edge cases

**Expected diagnosis:**

The function sorts the list but does not remove duplicates. Since the two largest values after sorting are both `7`, `nums[-2]` returns `7` instead of the second largest unique number, which is `5`.

**A strong corrected implementation:**

```python
def second_largest(nums):
    unique_nums = sorted(set(nums))

    if len(unique_nums) < 2:
        raise ValueError("At least two unique numbers are required.")

    return unique_nums[-2]
```

**Additional edge cases to test:**

```python
second_largest([5, 1, 7, 7, 3])   # 5
second_largest([1, 1, 1])         # error
second_largest([-1, -5, -3])      # -3
second_largest([2, 1])            # 1
```

### Harder Debugging Example: Moving Average

**Prompt:**

> This code sometimes crashes with:
>
> `IndexError: list index out of range`
>
> Identify the problem and fix it.

```python
def moving_average(values, window):
    result = []
    for i in range(len(values)):
        avg = sum(values[i:i+window]) / window
        result.append(avg)
    return result
```

**What this tests:**

* Debugging ability
* Edge case reasoning
* Understanding sliding windows
* Ability to explain what the code is supposed to do
* Ability to produce a safe implementation

**Important observation:**

The shown version using slicing does not normally raise an `IndexError`, because Python slices are safe even when they go past the end of the list. However, it does produce incorrect averages near the end because it divides by `window` even when fewer than `window` items are included.

A model should notice this inconsistency instead of blindly accepting the premise.

**Better fixed implementation:**

```python
def moving_average(values, window):
    if window <= 0:
        raise ValueError("Window size must be positive.")

    if window > len(values):
        return []

    result = []

    for i in range(len(values) - window + 1):
        avg = sum(values[i:i + window]) / window
        result.append(avg)

    return result
```

**Example:**

```python
moving_average([1, 2, 3, 4, 5], 3)
# [2.0, 3.0, 4.0]
```

**What a strong model should do:**

* Correctly identify that the loop goes too far
* Avoid partial windows unless requested
* Validate the window size
* Mention that slicing itself does not cause the `IndexError`
* Produce a clear corrected version

## 3.3 Explain Unfamiliar Code

### Example Test: Remove Duplicates While Preserving Order

**Prompt:**

> Explain what the following Python code does. Describe the algorithm, time complexity, and provide an example.
>
> Assume the reader is a junior developer.

```python
def transform(items):
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
```

**What this tests:**

* Code comprehension
* Teaching ability
* Technical communication
* Algorithm explanation
* Complexity analysis

**A strong answer should explain:**

This function removes duplicates from a list while preserving the order of the first occurrence of each item.

**Example:**

```python
transform(["apple", "banana", "apple", "orange", "banana"])
```

**Output:**

```python
["apple", "banana", "orange"]
```

**Expected complexity:**

* Time complexity: O(n), assuming set lookup is O(1) on average
* Space complexity: O(n), because the function stores seen items and the result list

## 3.4 Advanced Code Understanding

### Example Test: Merge Intervals

**Prompt:**

> Explain what problem this algorithm solves, walk through an example, and analyze its complexity.

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```

**What this tests:**

* Pattern recognition
* Algorithmic understanding
* Ability to explain non-trivial code
* Edge case awareness
* Complexity analysis

**A strong model should recognize:**

This is the standard “merge overlapping intervals” algorithm.

**Example input:**

```python
[[1, 3], [2, 6], [8, 10], [15, 18]]
```

**Expected output:**

```python
[[1, 6], [8, 10], [15, 18]]
```

**Walkthrough:**

1. Sort intervals by start time.
2. Start with the first interval.
3. Compare each new interval with the last merged interval.
4. If they overlap, combine them.
5. If they do not overlap, add the new interval separately.

**Complexity:**

* Sorting takes O(n log n)
* The merge pass takes O(n)
* Total time complexity is O(n log n)
* Space complexity is O(n) for the merged list

**Edge case a strong model should mention:**

The function will fail on an empty list because it uses `intervals[0]`. A more robust implementation should handle that case.

```python
def merge(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```

# 4. Personal Life Tasks

## 4.1 Travel Planning

### Task Types

The model should be able to:

* Build itineraries
* Estimate costs
* Suggest attractions
* Create packing lists
* Adapt to budget constraints

**Example prompt:**

> Plan a 5-day trip to Japan for under $1,500.

**What this tests:**

* Constraint handling
* Practicality
* Budget awareness
* Planning ability
* Organization

## 4.2 Cooking

### Task Types

The model should be able to:

* Suggest meals using ingredients on hand
* Create meal plans
* Scale recipes
* Handle dietary restrictions
* Reduce food waste

**Example prompt:**

> I have chicken, rice, onions, and spinach. What can I cook?

**What this tests:**

* Practical creativity
* Constraint satisfaction
* Step-by-step instruction
* Realistic cooking knowledge

## 4.3 Fitness

### Task Types

The model should be able to:

* Create workout plans
* Track progress
* Explain exercises
* Suggest recovery routines

**Example prompt:**

> Design a 3-day beginner strength program.

**What this tests:**

* Safety
* Progression
* Clarity
* Practicality
* Ability to tailor advice to experience level

## 4.4 Personal Finance

### Task Types

The model should be able to:

* Create budgets
* Analyze expenses
* Compare loans
* Explain investments
* Identify savings opportunities

**Example prompt:**

> Here is my monthly spending. Where can I save money?

**What this tests:**

* Numerical reasoning
* Practical judgment
* Risk awareness
* Clear explanation

## 4.5 Life Administration

### Task Types

The model should be able to:

* Write complaint letters
* Draft reimbursement requests
* Handle insurance paperwork
* Prepare tax questions
* Organize formal documents

**Example prompt:**

> Draft a letter requesting reimbursement from my airline.

**What this tests:**

* Formal writing
* Persuasiveness
* Clarity
* Practical usefulness

# 5. Advanced Knowledge Work

These tasks separate basic models from highly capable ones.

## 5.1 Research Assistant

**Example prompt:**

> Read these 10 papers and identify the common findings.

**Expanded version:**

> Read these 10 papers and produce:
>
> 1. A summary of the main findings
> 2. Areas where the papers agree
> 3. Areas where they disagree
> 4. Open research gaps
> 5. A short conclusion about what the evidence suggests overall

**What this tests:**

* Long-context reading
* Evidence synthesis
* Citation handling
* Identifying disagreement
* Avoiding unsupported claims

## 5.2 Strategic Planning

**Example prompt:**

> We’re a SaaS startup with slowing growth. Propose 3 strategies for the next 12 months.

**What this tests:**

* Business reasoning
* Prioritization
* Market analysis
* Scenario planning
* Ability to recommend practical actions

## 5.3 Expert Consulting

**Example prompt:**

> Should we migrate from PostgreSQL to ClickHouse?

**Expanded version:**

> Should we migrate from PostgreSQL to ClickHouse? Compare the options across:
>
> * Query performance
> * Data model fit
> * Engineering complexity
> * Cost
> * Operational risk
> * Migration difficulty
> * Long-term maintainability

**What this tests:**

* Technical judgment
* Tradeoff analysis
* Risk assessment
* Decision support
* Ability to avoid one-sided answers

## 5.4 Agentic Multi-Step Work

**Example prompt:**

> Analyze customer churn, identify causes, propose fixes, estimate impact, and generate a presentation.

**What this tests:**

* Long workflow execution
* Tool usage
* Multi-document reasoning
* Data interpretation
* Business writing
* End-to-end project completion

**A strong model should:**

* Break the task into steps
* Analyze the available data
* Identify likely causes
* Propose interventions
* Estimate impact carefully
* Produce a leadership-ready summary or deck

# 6. Recommended 25-Task Everyday LLM Evaluation Set

A balanced evaluation should include both simple everyday tasks and harder knowledge-work tasks.

## Office

1. Write a difficult professional email
2. Summarize a meeting transcript
3. Create a project plan
4. Analyze spreadsheet data
5. Generate SQL

## Education

6. Solve algebra
7. Solve calculus
8. Solve physics
9. Explain a concept simply
10. Debug student code

## Coding

11. Write code
12. Fix bugs
13. Review code
14. Design an API
15. Generate tests

## Personal

16. Plan a trip
17. Create a budget
18. Make a meal plan
19. Draft a complaint
20. Compare products

## Advanced

21. Analyze research papers
22. Build a business strategy
23. Evaluate tradeoffs
24. Detect contradictions in documents
25. Complete a multi-step project

A model that performs well on these tasks is likely useful in everyday work. A model that performs well on the advanced tasks is closer to being useful for delegated knowledge work, not just question answering.
