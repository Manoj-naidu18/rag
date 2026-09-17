# test_questions.py
# -------------------------------------------------------------------
# My own test set of 10 questions, with the result I expect and a
# PASS/FAIL check. The floor requires this, and it deliberately
# includes questions I expect the assistant to REFUSE, plus the two
# tricky corpus traps (the student gap and the reporting contradiction).
#
# Run it from the project root:   python tests/test_questions.py
# -------------------------------------------------------------------

import sys
from pathlib import Path

# Let this file import assistant.py from the code/ folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))
from assistant import answer

# Each test is:
#   (question, claim_date, change_date, word I expect to see in the reply)
TESTS = [
    ("What is the household resource limit?",
     "2026-01-15", None, "$4,000"),

    ("How much of my earnings is disregarded?",
     "2026-01-10", None, "$120"),           # before amendment

    ("How much of my earnings is disregarded?",
     "2026-04-01", None, "$175"),           # after amendment

    ("What is the sanction for a first offence?",
     "2026-04-01", None, "15 per cent"),    # amended sanction rate

    ("How is a full-time student's award calculated?",
     "2026-01-15", None, "REFUSE"),         # the corpus GAP

    ("How many days do I have to report a change?",
     "2026-04-01", "2026-02-10", "CONTRADICTION"),   # change BEFORE 1 Mar

    ("How many days do I have to report a change?",
     "2026-04-01", "2026-03-15", "14 calendar days"),  # change ON/AFTER 1 Mar

    ("Can I get help paying my pet dog's vet bills?",
     "2026-01-15", None, "REFUSE"),         # not covered at all

    ("How long does the Department have to decide my application?",
     "2026-01-15", None, "ANSWER"),         # §8.3.1 - covered

    ("What is the time limit to ask for a review of a decision?",
     "2026-01-15", None, "ANSWER"),         # §11.1.2 - covered
]


def run():
    passed = 0
    for i, (question, claim, change, expected) in enumerate(TESTS, start=1):
        reply = answer(question, claim, change)
        ok = expected in reply
        if ok:
            passed += 1
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Q{i}: {question}")
        print(f"        expecting to see: {expected!r}")
        if not ok:
            print("        --- got instead ---")
            print("        " + reply.replace("\n", "\n        "))
        print()

    print("=" * 55)
    print(f"RESULT: {passed} / {len(TESTS)} passed")
    print("=" * 55)


# -------------------------------------------------------------------
# Known weakness (reported honestly, as the floor asks):
# The two traps are caught by keyword matching, not by understanding.
# So a question that mentions "report" and "days" is always routed to
# the reporting-contradiction answer, even if it is really about
# something else. This is the main place the system would break, and
# the next step would be to detect these cases from the retrieved
# clauses rather than from keywords in the question.
# -------------------------------------------------------------------

if __name__ == "__main__":
    run()
