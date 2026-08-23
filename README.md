# Grounded Answer

This project is a command-line assistant for the Calder County Household Support Program.

It does three important things:

1. Answers policy questions from the supplied policy manual.
2. Shows the exact clauses used for each answer.
3. Refuses to guess when the manual does not answer the question.

The project also applies Amendment No. 2026-01. The amendment starts on 1 March 2026.

## Requirements

- Python 3.10 or newer
- No extra Python packages
- No internet connection

## Run the assistant

Open PowerShell in this folder and run:

```powershell
python assistant.py "What is the earnings disregard for a determination in April 2026?"
```

Example output:

```text
Answer: The household earnings disregard is $175 per month, applied once per household rather than once per earner.
Sources: §6.4.1(a), §6.4.2, Amendment No. 2026-01 §1.1, Amendment No. 2026-01 §5.1
```

You can also run `assistant.py` without a question:

```powershell
python assistant.py
```

The program will ask:

```text
Policy question:
```

This makes the file work with the VS Code Run button as well as with PowerShell arguments.

## Run the tests

Run:

```powershell
python evaluate.py
```

The test set contains ten questions. It checks old and new dates, updated values, normal answers, and a refusal case. The current result is:

```text
10/10 checks passed
```

## Date handling

The amendment changed different rules in different ways:

- Reporting deadlines use the date when the change happened.
- Earnings disregards, income thresholds, and sanctions use the determination date.
- A question about a date before 1 March 2026 uses the old rule.
- A question about a date on or after 1 March 2026 uses the amended rule.

The original manual is kept unchanged. Amendment citations are shown together with the original clause citations so the answer can be checked.

## Refusal behavior

The manual is the only source of policy. If it does not cover a question, the assistant does not use general knowledge or make up an answer.

For example:

```powershell
python assistant.py "Does the program pay childcare?"
```

The result is a refusal with a suggestion to ask a caseworker or supervisor. This is safer than giving an answer that sounds certain but is not supported by the manual.

## Project files

- `assistant.py` - reads the manual and answers supported questions
- `evaluate.py` - runs the ten-question test set
- `policy-manual.md` - the original policy manual
- `Amendment No. 2026-01.md` - the later policy amendment
- `DECISIONS.md` - design choices and the answer/refusal boundary
- `AI-USAGE.md` - a record of how AI assistance was used

## Clean run

The project can be copied or cloned into a new folder and run using only the commands above. It does not depend on files outside this project.
