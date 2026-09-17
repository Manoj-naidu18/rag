# BriteSpark

BriteSpark is a lightweight policy clause retrieval prototype for the Calder County Household Support Program manual. It converts the policy manual into individual, citation-aware clauses and retrieves the clauses most relevant to a user's natural-language question.

## How It Works

1. `code/read.py` reads `data/policy.md`.
2. Bold clause identifiers such as `**2.4.1**` are parsed into structured records.
3. The records are written to `data/clauses.json`.
4. `code/search.py` selects the clauses in force for the relevant date, creates vector embeddings with `all-MiniLM-L6-v2`, and indexes them with FAISS.
5. A question is converted into a vector and the three closest policy clauses are displayed with their citations and distances.

## Project Structure

```text
.
├── code/
│   ├── assistant.py    # Answers, refuses, or flags a contradiction
│   ├── read.py         # Extracts clauses from the policy manual
│   └── search.py       # Builds the clause index and runs searches
├── data/
│   ├── clauses.json    # Generated clause data
│   ├── policy.md       # Source policy manual
│   └── Amendment No. 2026-01.md
├── tests/
│   └── test_questions.py   # 10-question test set with pass/fail
└── requirements.txt    # Python dependencies
```

## The Assistant

`code/search.py` only finds the nearest clauses. `code/assistant.py` decides what to do with them and gives one of three outcomes:

- **Answer** — the manual covers the question, so it returns the governing clause and its citation.
- **Refuse** — the manual does not cover the question (or points at a rule that does not exist), so it says so and directs the user to a supervisor.
- **Contradiction** — the manual says two different things, so it shows both clauses instead of silently choosing one.

See `DECISIONS.md` for exactly where the line between answering and refusing is set, and why.

## Requirements

- Python 3.9 or newer
- Dependencies listed in `requirements.txt`

## Setup

From the project root:

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

The first search run downloads the `all-MiniLM-L6-v2` sentence-transformer model if it is not already available locally.

## Usage

Run these commands from the `code` directory because the scripts use paths relative to that directory.

### Build the clause file

```bash
cd code
python read.py
```

This regenerates `data/clauses.json` from `data/policy.md` and reports the number of clauses extracted.

### Search the policy

```bash
python search.py
```

Enter a natural-language question and the claim date when prompted, for example:

```text
What is the resource limit for a household?
```

Use ISO format (`YYYY-MM-DD`) for the claim date. For reporting questions, also enter the date on which the change occurred; press Enter when no change date applies. This matters because the amendment's reporting transition is based on the change date, while its other changes are based on the determination date.

The search prints the most relevant clauses, their policy citations, and FAISS distances. Lower distances indicate closer matches within the date-specific index. The function can also be called from Python as `search(question, claim_date, change_date=None, number=3)`.

### Run the assistant (answer / refuse / contradiction)

```bash
cd code
python assistant.py
```

Enter a question, a claim date, and (for reporting questions) the date the change occurred. The assistant replies with one of the three outcomes above.

### Run the test set

From the project root:

```bash
python tests/test_questions.py
```

This runs 10 questions — including ones the assistant is expected to refuse — and prints PASS/FAIL for each.

## Updating the Policy

1. Edit `data/policy.md` and preserve the clause format `**part.section.paragraph**`.
2. Keep formal amendments in `data/` and record their effective-date rules in the temporal selection layer.
3. From `code/`, run `python read.py` to regenerate `data/clauses.json`.
4. Run `python search.py` and verify representative questions against both historical and current dates.

The policy manual is fictional and includes its own statement that statute or regulation takes precedence where applicable. Search results should therefore be treated as retrieval assistance, not as a substitute for authoritative legal or administrative review.

## Current Status

The clause reader (`read.py`), the date-aware clause search (`search.py`), and the answer/refuse/contradiction assistant (`assistant.py`) are implemented, with a 10-question test set in `tests/`.