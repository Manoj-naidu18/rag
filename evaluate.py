"""Ten small checks for the policy assistant."""

from assistant import Assistant, Policy


TESTS = [
    ("February earnings disregard", "What is the earnings disregard for a determination in February 2026?", "$120", True),
    ("April earnings disregard", "What is the earnings disregard for a determination in April 2026?", "$175", True),
    ("Old reporting deadline", "How long do I have to report a change that happened in February 2026?", "10 calendar days", True),
    ("New reporting deadline", "How long do I have to report a change that happened on 10 April 2026?", "14 calendar days", True),
    ("New threshold", "What is the income threshold after March 2026?", "$1,225", True),
    ("New sanction", "What is the sanction for a failure to report in April 2026?", "15 per cent", True),
    ("Review deadline", "How long do I have to request a review?", "30 days", True),
    ("Evidence alternative", "Can the Department accept an alternative document?", "alternative evidence", True),
    ("Covered application", "How can I make an application?", "online", True),
    ("Unsupported cost", "Does the program pay childcare?", "Cannot answer from the manual", True),
    ("Student gap refusal", "How is a full-time student's award calculated?", "care allowance", True),
    ("Reporting conflict shown", "How long do I have to report a change that happened in February 2026?", "§9.1.4", True),
]


def main() -> int:
    assistant = Assistant(Policy(__import__("pathlib").Path("policy-manual.md")))
    passed = 0
    for name, question, expected, should_pass in TESTS:
        result = assistant.answer(question)
        actual_pass = expected.lower() in result.lower()
        status = "PASS" if actual_pass == should_pass else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"{status:4} {name}: {expected}")
    print(f"\n{passed}/{len(TESTS)} checks passed")
    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
