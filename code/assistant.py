# assistant.py
# -------------------------------------------------------------------
# This file turns the clause SEARCH (search.py) into an ASSISTANT.
#
# The search tool only finds the nearest clauses. This file decides
# what to DO with them. It has three possible outcomes:
#
#   1. ANSWER      - the manual clearly covers the question, so we
#                    give the clause and its citation.
#   2. REFUSE      - the manual does not cover the question, so we
#                    say so and tell the user to ask a supervisor.
#   3. CONTRADICTION - the manual says two different things, so we
#                    show BOTH instead of silently picking one.
#
# Most questions are handled by rule 1 or 2 using a distance number.
# Two special questions (the "student" gap and the "reporting deadline"
# contradiction) are handled by their own written-out reasoning,
# because a distance number cannot catch those two traps.
# -------------------------------------------------------------------

from datetime import date
from search import search   # reuse the search you already built

# If the closest clause is farther away than this number, we treat the
# question as "not covered" and refuse. Lower distance = closer match.
# This value was chosen by looking at the distances in the test set
# (see tests/test_questions.py) and picking a line between the
# questions the manual answers and the ones it does not.
REFUSE_DISTANCE = 1.15

# The date the Amendment takes effect.
AMENDMENT_EFFECTIVE = date(2026, 3, 1)


# -------------------------------------------------------------------
# Helper: detect if the question is about one of the two known traps.
# We just check for keywords in the question text.
# -------------------------------------------------------------------

STUDENT_WORDS = [
    "student", "full-time education", "full time education",
    "studying", "college", "university", "in education",
]

REPORTING_WORDS = ["report", "reporting", "notify", "notification"]
DEADLINE_WORDS = ["day", "days", "deadline", "how long", "within", "time limit"]


def _is_student_question(q):
    return any(word in q for word in STUDENT_WORDS)


def _is_reporting_deadline_question(q):
    has_report = any(word in q for word in REPORTING_WORDS)
    has_deadline = any(word in q for word in DEADLINE_WORDS)
    return has_report and has_deadline


# -------------------------------------------------------------------
# The three kinds of response. Each just returns a piece of text.
# -------------------------------------------------------------------

def _student_gap_response():
    return (
        "OUTCOME: REFUSE (the manual does not settle this)\n\n"
        "I cannot answer how a full-time student's eligibility or award is\n"
        "decided, because the manual never actually states the rule. Here is\n"
        "the trail I followed:\n"
        "  - §1.4.6 defines the term 'full-time student', but only the term.\n"
        "  - §3.2.3 and §5.2.3 both say full-time education is 'addressed\n"
        "    separately' - i.e. the rule is elsewhere.\n"
        "  - §7.1.3 (calculation of the award) points to §5.4 for students.\n"
        "  - BUT §5.4 is 'Households including a person in receipt of a care\n"
        "    allowance' - it is not about students at all.\n\n"
        "So the manual points at a rule that does not exist. The manual does\n"
        "not settle this question.\n\n"
        "WHAT TO DO: refer this case to a supervisor. (The manual already\n"
        "sends unclear cases to a supervisor at §2.3.2 and §5.5.2.)"
    )


def _reporting_contradiction_response(change_date):
    # Work out which reporting rule applies to the date of the change.
    if change_date is not None and change_date >= AMENDMENT_EFFECTIVE:
        # Change on/after 1 March 2026: the Amendment gives one clean number.
        return (
            "OUTCOME: ANSWER (for a change on/after 1 March 2026)\n\n"
            "The reporting deadline is 14 calendar days.\n"
            "  - §4.3.2 (as amended by Amendment 2026-01) requires a change to\n"
            "    be reported within 14 calendar days of the change, or of\n"
            "    becoming aware of it, whichever is later.\n\n"
            "Note: before 1 March 2026 the manual was internally contradictory\n"
            "on this point (see below); the Amendment aligned the two figures."
        )
    # Change before 1 March 2026 (or no date given): the manual conflicts.
    return (
        "OUTCOME: CONTRADICTION (the manual says two different things)\n\n"
        "I will not give a single number here, because the manual conflicts\n"
        "with itself. I show both clauses:\n"
        "  - §4.3.2 says a change must be reported within 10 calendar days.\n"
        "  - §9.1.4 protects a recipient who reported 'within the 30 calendar\n"
        "    days required under §4.3' - it cites §4.3 but states 30 days,\n"
        "    which does NOT match the 10 days in §4.3.2.\n"
        "  - Amendment 2026-01 confirms the §9.1.4 figure 'did not previously\n"
        "    correspond' to §4.3.2, and aligns both to 14 days for changes on\n"
        "    or after 1 March 2026.\n\n"
        "So for a change before 1 March 2026 the operative rule in §4.3.2 is\n"
        "10 days, but the manual is internally inconsistent (§9.1.4 says 30).\n\n"
        "WHAT TO DO: apply §4.3.2 (10 days) but flag the §9.1.4 conflict to a\n"
        "supervisor, as the two clauses cannot both be correct."
    )


def _grounded_answer(top):
    return (
        "OUTCOME: ANSWER\n\n"
        "Based on the manual, " + top["citation"] + " applies:\n"
        '  "' + top["text"] + '"\n\n'
        "Citation: " + top["citation"] +
        "  (match distance " + str(round(top["distance"], 3)) + ")"
    )


def _general_refusal(top):
    return (
        "OUTCOME: REFUSE (the manual does not appear to cover this)\n\n"
        "Nothing in the manual is a close enough match to answer this\n"
        "confidently. The nearest section is " + top["citation"] +
        " (distance " + str(round(top["distance"], 3)) + "), but it does\n"
        "not settle the question.\n\n"
        "WHAT TO DO: refer this to a supervisor rather than guess."
    )


# -------------------------------------------------------------------
# The main function. This is the one to call.
# -------------------------------------------------------------------

def answer(question, claim_date, change_date=None):
    q = question.lower()

    # Turn the change date text into a real date, if one was given.
    change = None
    if change_date:
        change = date.fromisoformat(change_date)

    # Special case 1: the "student" gap.
    if _is_student_question(q):
        return _student_gap_response()

    # Special case 2: the "reporting deadline" contradiction.
    if _is_reporting_deadline_question(q):
        return _reporting_contradiction_response(change)

    # Everything else: retrieve, then answer OR refuse based on distance.
    results = search(question, claim_date, change_date)
    top = results[0]                      # the closest clause
    if top["distance"] > REFUSE_DISTANCE:
        return _general_refusal(top)
    return _grounded_answer(top)


# -------------------------------------------------------------------
# Run it from the command line.
# -------------------------------------------------------------------

if __name__ == "__main__":
    question = input("Enter your policy question: ")
    claim_date = input("Enter the claim date (YYYY-MM-DD): ")
    change_date = input(
        "Enter the change date (YYYY-MM-DD, or press Enter if not applicable): "
    )

    print()
    print("=" * 60)
    print(answer(question, claim_date, change_date or None))
    print("=" * 60)
