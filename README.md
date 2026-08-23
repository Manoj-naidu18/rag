# Grounded Answer

This is a small command-line assistant for the Calder County Household Support Program. It answers selected policy questions from the supplied manual, names the exact clauses used, applies Amendment No. 2026-01 by date, and refuses questions the manual does not settle.

## Run it

Requires Python 3.10 or newer. No packages or network access are needed.

```text
python assistant.py "What is the earnings disregard for a determination in April 2026?"
python evaluate.py
```

The first command prints an answer and its sources. The second runs the ten-question evaluation and returns a non-zero exit code if a check fails.

## Design

`assistant.py` reads the numbered clauses from `policy-manual.md`. A small set of transparent topic handlers constructs answers from those clauses. Reporting uses the date of the change; earnings, thresholds, and sanctions use the date of determination. The amendment is cited alongside the original clause instead of changing the source file.

Questions outside the supported policy topics return `Cannot answer from the manual` and suggest a caseworker or supervisor. This prevents plausible general advice from being presented as county policy.

## Files

- `assistant.py` - the CLI and policy answer logic
- `evaluate.py` - ten checks, including refusal cases
- `policy-manual.md` and `Amendment No. 2026-01.md` - the corpus
- `DECISIONS.md` - design and refusal decisions
- `AI-USAGE.md` - how assistance was used
