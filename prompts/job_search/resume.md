# Resume Refinement Guide

Use this workflow to tailor an existing resume to a specific role while protecting factual accuracy. The goal is to improve positioning, clarity, and relevance, not to fabricate experience.

## Best for

- Tailoring a base resume to a job description
- Rewriting bullets with clearer impact and metrics
- Identifying missing keywords for applicant tracking systems
- Preparing a final proofreading pass before applying

## Expected output

- A prioritized edit plan mapped to the job description
- Suggested bullet rewrites based only on provided experience
- Keyword and skills recommendations separated by confidence level
- A final checklist for accuracy, clarity, and formatting

## Required input

- Base resume
- Target job description
- Role level or seniority
- Any constraints, such as one-page limit or no relocation
- Optional: list of accomplishments or metrics that are true but not yet in the resume

## Prepare Your Base Resume

- **Do NOT** generate a full resume from scratch.  
- **Create by hand**: Draft or update a core resume offline, listing your true experience, skills, education, and accomplishments.  

## Resume Template

Here is a resume template I'm using:

```tex
%-------------------------
% Simple Anonymous Resume Template
% License: MIT
%-------------------------
\documentclass[letterpaper,11pt]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}

%---------- SECTION FORMATTING ----------
\titleformat{\section}{\large\bfseries}{}{0em}{}[\vspace{4pt}\rule{\textwidth}{0.5pt}\vspace{-6pt}]
\setlist[itemize]{leftmargin=*,noitemsep,topsep=0pt}

%---------- PERSONAL INFO ----------
\newcommand{\Name}{Your Name}
\newcommand{\Email}{you@example.com}
\newcommand{\Phone}{(123) 456-7890}
\newcommand{\LinkedIn}{linkedin.com/in/username}
\newcommand{\GitHub}{github.com/username}

\begin{document}

%---------- HEADER ----------
\begin{center}
  {\LARGE \Name} \\
  \vspace{4pt}
  \Email{} $\vert$ \Phone{} $\vert$ \\
  \LinkedIn{} $\vert$ \GitHub{}
\end{center}

%---------- OBJECTIVE ----------
\section{Objective}
A concise statement of your career goals and what you bring to the role.

%---------- EXPERIENCE ----------
\section{Experience}
\begin{itemize}
  \item \textbf{Company Name, Location} \hfill Dates Employed
    \begin{itemize}
      \item Achievement or responsibility with quantifiable result.
      \item Another bullet highlighting impact or technology used.
    \end{itemize}
  \item \textbf{Previous Company, Location} \hfill Dates Employed
    \begin{itemize}
      \item Key accomplishment with metrics.
      \item Technology and methodologies employed.
    \end{itemize}
\end{itemize}

%---------- SKILLS ----------
\section{Skills}
\begin{itemize}
  \item \textbf{Programming:} Python, C++, JavaScript
  \item \textbf{Frameworks/Tools:} Django, Flask, Docker, Git, CI/CD
  \item \textbf{Databases:} PostgreSQL, MySQL, MongoDB
\end{itemize}

%---------- EDUCATION ----------
\section{Education}
\begin{itemize}
  \item \textbf{Degree, Major} \hfill Graduation Date
    \begin{itemize}
      \item Institution Name, Location
      \item Relevant coursework or honors.
    \end{itemize}
\end{itemize}

\end{document}
```

## Identify Mandatory and Optional Sections

**Mandatory Sections**:

- Contact Information (Name, Email, Phone, LinkedIn/Portfolio URL)
- Professional Summary or Objective
- Work Experience (Company, Role, Dates, Achievements)
- Education (Institution, Degree, Dates)
- Skills (Technical and Soft Skills)

**Optional Sections** (add if relevant):

- Certifications & Licenses
- Projects & Portfolio Highlights
- Publications or Presentations
- Volunteer & Leadership Activities
- Awards & Recognitions
- Languages & Interests

## Tailor to a Specific Job Description

```text
Act as a resume editor and hiring-screening advisor.

Goal: tailor my existing resume to the target job description without inventing facts.

Rules:
1. Use only information from my resume and the additional true facts I provide.
2. Do not create employers, degrees, dates, certifications, metrics, or responsibilities.
3. If a useful detail is missing, ask for it or mark it as [needs user input].
4. Separate strong matches from weak or missing matches.
5. Keep recommendations practical for a resume, not a career essay.

Return:
1. Top 10 job requirements from the posting.
2. Match analysis: requirement, evidence from my resume, gap, recommendation.
3. Suggested section order.
4. Skills and keywords to add only if they are supported by my experience.
5. Bullet rewrites using action verb + scope + method + result.
6. Claims that need verification before I use them.

Target job description:
"""
[PASTE JOB DESCRIPTION]
"""

My base resume:
"""
[PASTE RESUME]
"""

Additional true facts I can include:
"""
[OPTIONAL FACTS, METRICS, PROJECTS, TOOLS]
"""
```

## Bullet Rewrite Prompt

```text
Rewrite the resume bullets below for the target role.

Target role: [ROLE TITLE]
Tone: concise, specific, accomplishment-focused

Rules:
- Preserve the truth of each bullet.
- Do not add metrics unless I provided them.
- Prefer concrete verbs and measurable impact.
- Avoid buzzwords such as "results-driven", "passionate", and "dynamic".
- Keep each bullet under [NUMBER] words.

Return a table with:
Original bullet | Improved bullet | Why it is stronger | Any missing metric or fact to verify

Bullets:
"""
[PASTE BULLETS]
"""
```

## ATS Keyword Gap Prompt

```text
Compare my resume against the job description for keyword and skills alignment.

Return:
1. Keywords clearly present in my resume.
2. Keywords missing but supported by my experience.
3. Keywords missing and not supported by my experience.
4. Exact places where supported keywords could be added naturally.

Do not recommend adding unsupported skills.

Job description:
"""
[PASTE JOB DESCRIPTION]
"""

Resume:
"""
[PASTE RESUME]
"""
```

## Refine Iteratively

- **Incorporate suggestions** manually or via focused follow-up prompts.
- **Validate all changes** to ensure accuracy—never introduce false claims.
- **Adjust tone and length** per company culture (concise for startups, detailed for corporate).

## Final Checks

- Contact details are current and professional.
- Dates, titles, companies, and degrees are accurate.
- Skills listed are supported by experience.
- Bullets emphasize impact, scope, tools, and outcomes.
- Formatting is consistent and readable after export to PDF.
- No claim was added solely because it appeared in the job description.
