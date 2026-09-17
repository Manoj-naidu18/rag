import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "data" / "policy.md"

# Read the policy
with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Keep lists and tables belonging to a clause until the next clause starts.
pattern = r"\*\*(\d+\.\d+\.\d+)\*\*\s*(.*?)(?=\n\n(?:\*\*\d+\.\d+\.\d+\*\*|#+ )|\n---|\Z)"

matches = re.findall(pattern, text, re.DOTALL)

clauses = []

for number, content in matches:
    content = content.replace("**", "")
    content = " ".join(content.split())

    clauses.append({
        "id": number,
        "citation": f"§{number}",
        "text": content,
        "source": "consolidated manual",
        "effective_from": "0001-01-01",
        "effective_to": "2026-02-29"
    })

# Save the clauses
with open(ROOT / "data" / "clauses.json", "w", encoding="utf-8") as f:
    json.dump(clauses, f, indent=2, ensure_ascii=False)

print("Policy reading completed!")
print(f"Total clauses found: {len(clauses)}")
print("Saved to: data/clauses.json")