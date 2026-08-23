"""A small, date-aware policy question assistant."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent
DEFAULT_DATE = date(2026, 8, 23)
AMENDMENT_DATE = date(2026, 3, 1)


@dataclass(frozen=True)
class Clause:
    number: str
    text: str


class Policy:
    def __init__(self, path: Path) -> None:
        self.clauses = self._read_clauses(path)
        self.by_number = {clause.number: clause for clause in self.clauses}

    @staticmethod
    def _read_clauses(path: Path) -> list[Clause]:
        clauses: list[Clause] = []
        pattern = re.compile(r"^\*\*(\d+\.\d+\.\d+[A-Z]?)\*\*\s*(.*)$")
        for line in path.read_text(encoding="utf-8").splitlines():
            match = pattern.match(line.strip())
            if match:
                clauses.append(Clause(match.group(1), match.group(2).strip()))
        return clauses

    def text(self, number: str) -> str:
        return self.by_number[number].text


class Assistant:
    def __init__(self, policy: Policy) -> None:
        self.policy = policy

    def answer(self, question: str) -> str:
        asked_date = find_date(question) or DEFAULT_DATE
        lowered = question.lower()

        if any(word in lowered for word in ("childcare", "child care", "medical bill", "rent", "legal aid")):
            return refuse("The manual does not say that the Program pays that particular cost. Ask a caseworker at a district office whether another program applies.")

        if "sanction" in lowered:
            return self._sanction_answer(asked_date)
        if any(word in lowered for word in ("report", "reporting", "change of circumstance", "change in circumstances")):
            return self._reporting_answer(asked_date)
        if "overpayment" in lowered or "recover" in lowered:
            return self._overpayment_answer(asked_date)
        if any(word in lowered for word in ("earnings disregard", "earned income", "earnings")):
            return self._earnings_answer(asked_date)
        if any(word in lowered for word in ("threshold", "income limit", "income limits")):
            return self._threshold_answer(asked_date)
        if "appeal" in lowered or "review" in lowered:
            return self._review_answer()
        if "evidence" in lowered or "document" in lowered:
            return self._evidence_answer()
        if "resource" in lowered or "savings" in lowered:
            return self._resources_answer()
        if "application" in lowered or "apply" in lowered:
            return self._application_answer()

        return refuse("The manual does not contain enough information to answer that question. Ask a supervisor or a caseworker to interpret the case.")

    def _reporting_answer(self, change_date: date) -> str:
        if change_date >= AMENDMENT_DATE:
            return answer(
                "Report the change within 14 calendar days of it happening, or within 14 calendar days of becoming aware of it, whichever is later. The report can be made in person, by telephone, in writing, or online.",
                ["§4.3.2", "§4.3.3", "Amendment No. 2026-01 §2.1", "Amendment No. 2026-01 §5.2"],
            )
        return answer(
            "For a change occurring before 1 March 2026, the reporting period was 10 calendar days from the change or from becoming aware of it, whichever was later.",
            ["§4.3.2", "Amendment No. 2026-01 §5.2"],
        )

    def _overpayment_answer(self, change_date: date) -> str:
        if change_date >= AMENDMENT_DATE:
            return answer(
                "Where the overpayment arose from a change of circumstances, reporting within 14 calendar days means that no overpayment is established for the period before the Department was in a position to act on the report.",
                ["§9.1.3", "§9.1.4", "Amendment No. 2026-01 §2.2", "Amendment No. 2026-01 §5.2"],
            )
        return answer(
            "For a change occurring before 1 March 2026, the corresponding reporting period was 10 calendar days. If the change was reported within that period, §9.1.4 says no overpayment is established before the Department was in a position to act.",
            ["§4.3.2", "§9.1.4", "Amendment No. 2026-01 §5.2"],
        )

    def _earnings_answer(self, determination_date: date) -> str:
        amount = "$175" if determination_date >= AMENDMENT_DATE else "$120"
        citations = ["§6.4.1(a)", "§6.4.2"]
        if determination_date >= AMENDMENT_DATE:
            citations += ["Amendment No. 2026-01 §1.1", "Amendment No. 2026-01 §5.1"]
        return answer(f"The household earnings disregard is {amount} per month, applied once per household rather than once per earner.", citations)

    def _threshold_answer(self, determination_date: date) -> str:
        threshold = "$1,225 for one member, then $425 for each additional member" if determination_date >= AMENDMENT_DATE else "$1,180 for one member, then $410 for each additional member"
        citations = ["§6.6.1"]
        if determination_date >= AMENDMENT_DATE:
            citations += ["Amendment No. 2026-01 §3.1", "Amendment No. 2026-01 §5.1"]
        return answer(f"The monthly income threshold is {threshold}.", citations)

    def _sanction_answer(self, determination_date: date) -> str:
        if determination_date >= AMENDMENT_DATE:
            return answer("A first sanction reduces the monthly award by 15 per cent for 4 weeks; a subsequent sanction within 12 months lasts 8 weeks. A sanction must not be imposed for an unreported change that would have increased the award.", ["§10.5.1", "§10.5.3", "Amendment No. 2026-01 §4.1", "Amendment No. 2026-01 §4.2", "Amendment No. 2026-01 §5.1"])
        return answer("Before 1 March 2026, a first sanction reduced the monthly award by 20 per cent for 4 weeks; a subsequent sanction within 12 months lasted 8 weeks.", ["§10.5.1", "§10.5.2", "§10.5.3"])

    def _review_answer(self) -> str:
        return answer("A review request must be made within 30 days of the determination notice. It may be made in any form, including orally, and the review must be done by an officer who was not involved in the original decision.", ["§11.1.1", "§11.1.2", "§11.1.3", "§11.2.1"])

    def _evidence_answer(self) -> str:
        return answer("The applicant must provide evidence of identity, residence, income, and resources. The Department must consider alternative evidence and must give at least 14 days to supply requested evidence, extending that period on request when reasonable steps are being taken.", ["§8.2.1", "§8.2.2", "§8.2.3"])

    def _resources_answer(self) -> str:
        return answer("A household is not eligible when countable resources exceed $4,000. The home, one motor vehicle, household goods, and some other listed items are not countable resources.", ["§2.4.1", "§2.4.2"])

    def _application_answer(self) -> str:
        return answer("An application may be made online, in person, by telephone, or in writing. It is valid when it contains the applicant's name and address, household composition, and a signature or electronic equivalent.", ["§8.1.1", "§8.1.2"])


def answer(text: str, citations: list[str]) -> str:
    citation_text = ", ".join(citations)
    return f"Answer: {text}\nSources: {citation_text}"


def refuse(text: str) -> str:
    return f"Cannot answer from the manual: {text}\nSources: none"


def find_date(text: str) -> date | None:
    patterns = [
        r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",
        r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        values = [int(value) for value in match.groups()]
        if len(str(values[0])) == 4:
            year, month, day = values
        else:
            day, month, year = values
        try:
            return date(year, month, day)
        except ValueError:
            return None

    month_match = re.search(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(202[5-6])\b", text, re.IGNORECASE)
    if month_match:
        month = datetime.strptime(month_match.group(1), "%B").month
        return date(int(month_match.group(2)), month, 1)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Answer one Calder County policy question.")
    parser.add_argument("question", nargs="*", help="the policy question")
    args = parser.parse_args()
    if not args.question:
        typed_question = input("Policy question: ").strip()
        if not typed_question:
            parser.error("enter a policy question")
        args.question = typed_question.split()
    policy = Policy(ROOT / "policy-manual.md")
    print(Assistant(policy).answer(" ".join(args.question)))


if __name__ == "__main__":
    main()
