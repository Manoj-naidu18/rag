import json
from datetime import date
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
AMENDMENT_EFFECTIVE = date(2026, 3, 1)

# Load policy clauses
with open(ROOT / "data" / "clauses.json", "r", encoding="utf-8") as f:
    clauses = json.load(f)

AMENDED_CLAUSES = {
    "§6.4.1": {
        "text": "The first $175 per month of household earnings from employment is disregarded.",
        "basis": "determination"
    },
    "§6.6.1": {
        "text": "A household is not eligible where countable income exceeds the applicable threshold. The thresholds are $1,225 for one member, $1,650 for two members, $2,075 for three members, $2,500 for four members, $2,925 for five members, and $425 for each additional member.",
        "basis": "determination"
    },
    "§10.5.2": {
        "text": "A sanction is a reduction of the monthly award by 15 per cent for a period of 4 weeks for a first sanction, or 8 weeks for a subsequent sanction within 12 months.",
        "basis": "determination"
    },
    "§10.5.3A": {
        "text": "A sanction must not be imposed in respect of a failure to report where the change of circumstances in question would have increased the award.",
        "basis": "determination"
    },
    "§4.3.2": {
        "text": "A recipient must report any change in household composition, income, address, or the circumstances of any household member within 14 calendar days of the change occurring, or within 14 calendar days of the recipient becoming aware of the change, whichever is later.",
        "basis": "change"
    },
    "§9.1.4": {
        "text": "Where an overpayment has arisen from a change of circumstances, and the recipient reported the change within the 14 calendar days required under §4.3, no overpayment shall be established in respect of any period before the date on which the Department was in a position to act on the report.",
        "basis": "change"
    }
}

LEGACY_FOCUSED_TEXT = {
    "§6.4.1": "The first $120 per month of household earnings from employment is disregarded.",
    "§6.6.1": "A household is not eligible where countable income exceeds the applicable threshold. The thresholds are $1,180 for one member, $1,590 for two members, $2,000 for three members, $2,410 for four members, $2,820 for five members, and $410 for each additional member.",
    "§10.5.2": "A sanction is a reduction of the monthly award by 20 per cent for a period of 4 weeks for a first sanction, or 8 weeks for a subsequent sanction within 12 months.",
    "§4.3.2": "A recipient must report any change in household composition, income, address, or the circumstances of any household member within 10 calendar days of the change occurring, or within 10 calendar days of becoming aware of the change, whichever is later.",
    "§9.1.4": "Where an overpayment has arisen from a change of circumstances, and the recipient reported the change within the 30 calendar days required under §4.3, no overpayment shall be established before the Department was in a position to act on the report."
}


def _parse_date(value, name):
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be an ISO date in YYYY-MM-DD format") from error


def _clauses_for_date(claim_date, change_date=None):
    claim_date = _parse_date(claim_date, "claim_date")
    change_date = _parse_date(change_date or claim_date, "change_date")
    selected = []

    for clause in clauses:
        amendment = AMENDED_CLAUSES.get(clause["citation"])
        relevant_date = change_date if amendment and amendment["basis"] == "change" else claim_date
        if amendment and relevant_date >= AMENDMENT_EFFECTIVE:
            continue
        if clause["citation"] in LEGACY_FOCUSED_TEXT:
            clause = {**clause, "text": LEGACY_FOCUSED_TEXT[clause["citation"]]}
        selected.append(clause)

    for citation, amendment in AMENDED_CLAUSES.items():
        relevant_date = change_date if amendment["basis"] == "change" else claim_date
        if relevant_date >= AMENDMENT_EFFECTIVE:
            selected.append({
                "id": citation.lstrip("§"),
                "citation": citation,
                "text": amendment["text"],
                "source": "Amendment No. 2026-01",
                "effective_from": AMENDMENT_EFFECTIVE.isoformat(),
                "effective_to": None
            })

    return selected

# Load embedding model
print("Loading search model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(question, claim_date, change_date=None, number=3):
    """
    Search the policy in force for a claim date.

    Reporting rules use change_date because Amendment No. 2026-01 gives
    those rules a different transitional basis from the other amendments.
    """
    active_clauses = _clauses_for_date(claim_date, change_date)
    active_texts = [clause["text"] for clause in active_clauses]
    active_vectors = model.encode(active_texts)
    active_vectors = np.array(active_vectors).astype("float32")
    active_index = faiss.IndexFlatL2(active_vectors.shape[1])
    active_index.add(active_vectors)

    # Convert question into a vector
    question_vector = model.encode([question])
    question_vector = np.array(question_vector).astype("float32")

    # Search
    distances, positions = active_index.search(question_vector, min(number, len(active_clauses)))

    results = []

    for distance, position in zip(distances[0], positions[0]):
        clause = active_clauses[position]

        results.append({
            "citation": clause["citation"],
            "text": clause["text"],
            "distance": float(distance)
        })

    return results


# Test the search
if __name__ == "__main__":

    question = input("Enter your policy question: ")
    claim_date = input("Enter the claim date (YYYY-MM-DD): ")
    change_date = input("Enter the change date (YYYY-MM-DD, or press Enter if not applicable): ")

    results = search(question, claim_date, change_date or None)

    print("\nRelevant policy clauses:\n")

    for result in results:
        print("----------------------------------------")
        print("Citation:", result["citation"])
        print("Distance:", round(result["distance"], 4))
        print("Policy:", result["text"])

    print("----------------------------------------")