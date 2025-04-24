# Interview Questions Study Guide

Use this structured workflow to transform a job description into a comprehensive set of interview questions and practice answers. Export your results in CSV format for easy tracking.

## Extract Key Topics from Job Description

1. **Paste** the full job description into your LLM prompt.  
2. **Prompt**:

```text
"Analyze the following job description and list 8–10 distinct topic categories a candidate should prepare for."
```

3. **Output**: A numbered list of topics (e.g., "Product Strategy", "Data Analysis", "Team Leadership").

## Generate Common Interview Questions

For each topic category identified:

1. **Prompt**:
   
```text
"Based on the job description and the topic '[TOPIC]', generate the 20 most common interview questions employers ask."  
```

2. **Tip**: Use batch prompts to cover multiple categories at once or iterate one by one to stay focused.

## Create a Practice Answer Study Guide

1. **Select** the top 5–10 questions you want to practice first.  
2. **Prompt for STAR Answers**:  

```text
"For each of the following questions, write a concise answer using the STAR format (Situation, Task, Action, Result):
1. [Question 1]
2. [Question 2]
...
```

3. **Alternate Formats**: You can ask for other structures (e.g., CAR: Context, Action, Result) by updating the prompt.

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
