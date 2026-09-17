# AI Usage

This file records how AI tools were used in building this project, as required by the Brite Spark 2026 rules. I have tried to be straightforward about it: AI was used as an assistant, and I remain responsible for understanding, testing, and standing behind everything in the repository.

## Tools used

- **ChatGPT** and **GitHub Copilot** — used as coding and explanation assistants throughout.

## What AI was used for

**Design discussion.** I described the problem (grounded answers, a refusal path, the two corpus traps) and used AI to talk through approaches — retrieval by embeddings, where to draw the line between answering and refusing, and how to keep retrieval, answer construction, and refusal separable.

**Code generation and editing.** AI helped write and refactor the Python:
- `code/read.py` — parsing the manual into citation-tagged clauses.
- `code/search.py` — the date-aware clause selection and the embedding/FAISS search.
- `code/assistant.py` — the answer / refuse / contradiction layer on top of the search.
- `tests/test_questions.py` — the 10-question test set.

**Documentation.** AI helped draft `README.md`, `DECISIONS.md`, and this file, based on decisions I made.

**Explanation.** I used AI to explain how each part works in plain language so that I understand it well enough to defend it, rather than treating any of it as a black box.

## What I did myself

- Chose the overall approach and the three-outcome design (answer / refuse / contradiction).
- Decided **where to set the refusal threshold** (a match distance of 1.15) after looking at the actual distances the search returned on my own test questions — real answers landed around 0.55–0.70, an uncovered question at 1.33, so 1.15 sits in the gap.
- Decided that the two corpus traps (the student "gap" and the reporting-deadline contradiction) needed explicit handling, because a similarity score cannot catch a cross-reference that points to the wrong section.
- Wrote the test questions to deliberately include cases the system should refuse, and reported the results honestly.
- Ran the code, checked the outputs against the manual clause by clause, and confirmed the temporal (date-based) answers were correct.

## How I checked the AI's output

I did not accept generated code or answers on trust:
- I ran the assistant against the real data pack and read every clause it cited back in `data/policy.md` to confirm it was quoting the manual correctly.
- I verified the date logic by asking the same question for a date before and after 1 March 2026 and checking the figures against the Amendment.
- I ran the full test set and confirmed the pass/fail results myself.

## Honest limitations

- The two special cases (student, reporting deadline) are recognised by **keyword matching** on the question, not by reasoning over the retrieved clauses. This works but is brittle, and it is the first thing I would rebuild. It is recorded as a known weakness in `DECISIONS.md` and in my own testing notes.
- The plain-language "answer" is the clause text itself shown with its citation, not a paraphrase. I chose this deliberately so that an answer can never drift from the source — but it means answers read like policy text rather than conversational language.

## Integrity statement

AI helped me build this faster and understand it better, but the design choices, the testing, and the judgement calls — especially where to answer and where to refuse — are mine, and I can explain any part of the code and defend the decisions behind it.
