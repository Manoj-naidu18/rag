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

The test set contains twelve questions. It checks old and new dates, updated values, normal answers, a refusal case, the full-time student gap, and the reporting-deadline conflict. The current result is:

```text
12/12 checks passed
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

Some questions look covered but are not. For a full-time student the assistant does not give a generic refusal; it shows the trail it followed:

```powershell
python assistant.py "How is a full-time student's award calculated?"
```

It reports that §1.4.6 only defines the term, §3.2.3 and §5.2.3 say full-time education is "addressed separately", and §7.1.3 sends the case to §5.4 - but §5.4 is about a care allowance, not students. The pointer leads to the wrong topic, so the manual does not settle it, and the case goes to a supervisor.

## Conflicts in the manual

The manual is internally inconsistent about the reporting deadline for a change before 1 March 2026. §4.3.2 says 10 calendar days; §9.1.4 refers to "the 30 calendar days required under §4.3". The assistant does not pick one silently - it shows both figures, notes that Amendment No. 2026-01 confirms they "did not previously correspond" and aligns them to 14 days from 1 March 2026, and points to §4.3.2 as the operative rule while flagging the conflict.

## Project files

- `assistant.py` - reads the manual and answers supported questions
- `evaluate.py` - runs the ten-question test set
- `policy-manual.md` - the original policy manual
- `Amendment No. 2026-01.md` - the later policy amendment
- `DECISIONS.md` - design choices and the answer/refusal boundary
- `AI-USAGE.md` - a record of how AI assistance was used

## Clean run

The project can be copied or cloned into a new folder and run using only the commands above. It does not depend on files outside this project.
