# Decisions

## 2026-08-23: Amendment No. 2026-01

### Changed

- Added `data/Amendment No. 2026-01.md` to the policy corpus.
- Added effective-date metadata to clauses generated from the consolidated manual.
- Added amendment variants for the earnings disregard, income thresholds, sanction rules, and reporting rules.
- Changed clause retrieval to require an ISO `claim_date` and select the rule in force for that date.
- Added an optional `change_date`; reporting amendments use this date because the amendment's transitional provision applies to the date the change occurred, not the determination date.
- Made script data paths resolve from the repository, so commands work regardless of the caller's current directory.

### Chosen not to change

- The consolidated manual remains unchanged as the historical source text.
- The existing FAISS and sentence-transformer approach remains in place.
- No answer-generation or web application layer was added because `app.py` is still empty and the current working feature is clause retrieval.
- Unaffected clauses were not duplicated as amendment variants.

### With hindsight

I would have introduced effective-date metadata when the initial clause index was created. The original implementation assumed that the latest loaded corpus was always current, which made historical questions impossible to answer reliably once an amendment arrived.

## 2026-09-16: Answer, refusal and contradiction layer (`code/assistant.py`)

### Changed

- Added `code/assistant.py`, which sits on top of the existing clause search and produces one of three outcomes for each question: **answer**, **refuse**, or **contradiction**.
- Added a 10-question test set in `tests/test_questions.py` with pass/fail, including questions the assistant is expected to refuse.

### Where I set the line between answering and refusing

There are two different refusal mechanisms, because one number cannot catch every case:

1. **General refusal by distance.** For an ordinary question I retrieve the nearest clause. If the closest match has an L2 distance **above 1.15**, I treat the manual as not covering the question and refuse. I chose 1.15 by looking at the distances in the test set: clauses the manual genuinely answers came back at roughly 0.55–0.70, while a question the manual does not cover (help with a pet's vet bills) came back at 1.33. 1.15 sits in the empty gap between those two groups, so it is a defensible line rather than an arbitrary one. The trade-off: set it lower and the system refuses things it could answer; set it higher and it starts answering things it should not.

2. **Explicit reasoning for the two corpus traps.** A distance score cannot catch the two situations the problem was really about, because in both the retriever returns confident-looking passages:
   - **The student gap.** §7.1.3 points to §5.4 for students, but §5.4 is about care allowances, so the rule never actually exists. The assistant walks this cross-reference trail out loud and then refuses to a supervisor, instead of giving a generic "not enough information".
   - **The reporting-deadline contradiction.** §4.3.2 says 10 days; §9.1.4 cites §4.3 but states 30; the Amendment confirms they never matched. The assistant surfaces **both** clauses rather than silently picking one, and is date-aware: a change on/after 1 March 2026 gets the clean 14-day answer, a change before that gets the contradiction.

### Known weakness

The two traps are recognised by keyword matching on the question, not by reasoning over the retrieved clauses. So a question that merely mentions "report" and "days" is always routed to the reporting answer. The honest next step is to detect these two situations from the retrieved clauses themselves, keeping retrieval, answer construction and refusal separable — which is also what the day-two warning was pushing towards.
