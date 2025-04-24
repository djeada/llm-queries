# Sanitize LaTeX  
Use these prompt templates to guide an LLM in cleaning up LaTeX by stripping out unnecessary spacing commands, redundant delimiters, and repeated punctuation.

## Base Cleanup Prompt  

**Prompt:**  

```text
Clean the following LaTeX code by removing all unnecessary spacing macros (for example '\,' or '\;'), redundant surrounding characters around operators (such as '\;=\;'), and any repeated punctuation marks (like ',,'). After cleaning, each operator should appear in its standard form (for example '=' or '<') with a single space on either side, and there should be no trailing punctuation inside math delimiters. Preserve valid LaTeX syntax and equation structure.
```

**Example Before:**

$$\;=\;$$

**After Cleaning:**  

$$=$$

## Complex Equation Example  

**Prompt:**

```text
Apply the same cleanup rules to this equation. Remove all '\,' spacing commands, extra delimiters, and trailing punctuation.
```

**Before:**  

$$R_{it} 
,\equiv, \frac{D_{it} + P_{it} - P_{it-1}}{P_{it-1}} 
,=, \frac{D_{it} + P_{it}}{P_{it-1}} - 1$$

**After Cleaning:**  

$$R_{it} 
\equiv \frac{D_{it} + P_{it} - P_{it-1}}{P_{it-1}} 
= \frac{D_{it} + P_{it}}{P_{it-1}} - 1$$

## Variable and Operator Spacing  

**Prompt:**

```text
Remove any '\,' before variables or operators so that sequences like '\,dx' become 'dx' and '\,<\,' become '<'.
```

Before:

$$\int f(x)\,dx \quad\text{and}\quad a \,<\, b$$

After:

$$\int f(x) dx \quad\text{and}\quad a < b$$

## Trailing Punctuation Removal  

**Prompt:**  

```text
Eliminate trailing punctuation inside math delimiters. For instance, convert '$$equation .$$' or '$equation ,$' into '$equation$'.
```

Before

$$E = mc^2 .$$

After

$$E = mc^2$$
