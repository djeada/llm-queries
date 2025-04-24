# Resume Refinement Guide

Use this workflow to iteratively improve your existing resume with an LLM, tailoring it to each job without fabricating information.

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

1. **Paste** the job description into your prompt.  
2. **Prompt**:
   ```text
   "Review my base resume and the following job description. Suggest which experiences, keywords, and metrics I should emphasize or reorder to match this role."
   ```
3. **LLM Output**: A list of bullet suggestions, e.g.:
   - Move `Project X` above `Internship Y` to highlight relevant skills.  
   - Add keyword `data visualization` under Skills.  
   - Quantify results: change “improved efficiency” to “improved efficiency by 30%.”

## Refine Iteratively

- **Incorporate suggestions** manually or via follow-up prompts:
  - Prompt: "Rewrite my Work Experience bullets using action verbs and metrics."
- **Validate all changes** to ensure accuracy—never introduce false claims.
- **Adjust tone and length** per company culture (concise for startups, detailed for corporate).

## Final Checks

- **Proofread** for grammar and consistency.  
- **Verify dates and facts** against original sources.  
- **Ask the LLM**: "Scan for any typos or inconsistencies in this resume."  

