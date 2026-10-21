
# TD1 Report - Evaluating Language Models

**Course:** Trustworthy Generative AI - ESILV  
**Date:** October 21, 2026  
**Subgroup:** To be added  
**Members:** To be added

## 1. Objective

The goal of TD1 is to evaluate how reliably five language models generate SQL queries to answer questions about an e-commerce database.

We compare their results against reference answers calculated directly using SQL.

We also study model errors, execution times, API limitations and costs.

## 2. Environment

- Python: 3.14.6
- Database: SQLite (`boutique.sqlite`)
- Student kit: `2026-10-18-students-1`
- Providers: Groq and OpenRouter
- Models: Three Groq models and two OpenRouter models

The database integrity check passed successfully.

The API preparation check also returned 5/5 models OK using the original working environment.

This confirms API access, not completion of the experiments.

## 3. SQL Reference Calculations

We must calculate 20 reference answers using SQL and have them independently verified before comparing them with model outputs.

### My contribution: C07, C08 and C09

I was responsible for writing and executing the SQL queries for questions C07, C08 and C09.

| Question | Revenue (cents) | Status |
|---|---:|---|
| C07 | 13970 | Calculated, awaiting verification |
| C08 | 605580 | Calculated, awaiting verification |
| C09 | 487980 | Calculated, awaiting verification |

**C07:** Calculate revenue for orders placed on May 31, 2026.

**C08:** Calculate revenue from all orders made by customers who were exactly 25 years old on September 24, 2026.

**C09:** Calculate revenue from all orders made by customers who were exactly 25 years old on September 26, 2026.

The SQL queries and calculated values are saved in [reference-td1.csv](../kit-td1/reference-td1.csv).

Independent verification by another group member is still pending.

### Remaining references

To be completed by the other group members.

## 4. Model Experiments

We will test five language models using the same 20 questions.

For each model, we will record:

- Generated SQL queries
- Correct and incorrect answers
- API errors and retries
- Response times and available measurements
- Raw traces and execution results

**Status:** Pending group experiments.

The completed experiment files and trace links will be added here.

## 5. Model Comparison

After the experiments, we will compare the five models based on their results.

The comparison will cover correctness, common SQL mistakes, reliability and available performance measurements.

**Status:** Pending experimental results.

## 6. Errors and Difficulties

We will document any problems encountered during the TD, including failed requests, incorrect SQL, missing measurements and API limitations.

For each issue, we will distinguish what we observed from our explanation of its possible cause.

**Status:** To be completed using actual experimental evidence.

## 7. Limitations

At this stage:

- Not all 20 reference answers have been completed.
- C07, C08 and C09 have not yet been independently verified.
- The model comparison experiments are pending.
- No conclusions about model performance can be drawn yet.

Any missing data or fallback traces will be clearly identified.

## 8. Team Contributions

| Member | Contribution |
|---|---|
| Jawed FERHAT | SQL reference calculations for C07, C08 and C09 |
| Other members | To be added |

The final division of model experiments, verification and analysis will be documented after the session.

## 9. Next Steps

- Complete all 20 SQL references.
- Independently verify the results.
- Run the allocated model batches.
- Save the raw traces and experiment results.
- Complete the comparison CSV files.
- Analyze errors and model performance.
- Finalize the report and GitHub submission.

## 10. AI Assistance

AI assistance was used to help prepare SQL queries and organize the repository documentation.

The SQL queries were executed against the provided database. Independent student verification is still required.

The prompts used will be retained as part of the project documentation.

