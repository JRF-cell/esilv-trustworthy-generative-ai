# Trustworthy Generative AI

ESILV | A4 Data & AI | 2026–2027

This repository contains our work for the Next-Generation AI course at ESILV.

The goal is to evaluate how reliably different language models generate SQL queries. We compare their answers with reference results calculated directly from a SQLite database.

## Team

- Subgroup: To be added
- Members: To be added

## TD1: Evaluating Language Models

For TD1, we compare five language models on 20 questions about sales revenue.

Our work consists of:
1. Writing SQL queries to calculate the correct answers.
2. Independently verifying these reference results.
3. Running the same questions through five AI models.
4. Comparing the results and analyzing errors, response times and costs.

The five models are accessed through Groq and OpenRouter.

## TD2 and TD3

The same repository will be used for TD2 and TD3. Their work and reports will be added after each session.

## Project Structure

- `kit-td1/`: Official student kit, SQLite database, Python scripts and experiment files.
- `reports/`: Reports for each TD.
- `README.md`: Project information and setup instructions.

## Setup

Requirements:
- Python 3.10 or newer
- The `requests` Python package
- Free Groq and OpenRouter accounts

From the repository root:

```bash
cd kit-td1
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install requests
python3 verify-data.py
```

The verification should return `"ok": true`.

To check access to the five AI models, first configure the `GROQ_API_KEY` and `OPENROUTER_API_KEY` environment variables following the official environment guide.

Then run:

```bash
python3 check_access.py | tee ready-for-td1.txt
```

This command makes five API requests. API keys must never be committed to GitHub.

The commands for running the TD1 experiments and reproducing the results will be documented as the group completes the work.

## Technical Information

- Course pack: `2026-10-18-students-1`
- Python version used: 3.14.6
- Database: SQLite (`boutique.sqlite`)
- Providers: Groq and OpenRouter

Database SHA-256:

`0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`

## Current Progress

- [x] Downloaded the official October 18 student kit.
- [x] Verified database integrity.
- [x] Calculated and saved SQL answers for C07, C08 and C09.
- [ ] Independently verify these answers with teammates.
- [ ] Complete the remaining SQL references.
- [ ] Run the model experiments.
- [ ] Analyze results and complete `reports/td1.md`.

## AI Assistance

AI tools were used to help prepare the repository and write SQL queries. The group is responsible for checking the results and documenting the prompts used.

## References

- [Course website](https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/index.html)
- [TD1 instructions](https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/students/kit-td1/enonce-td1-en.html)
- [Submission requirements](https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/students/submission-en.html)
