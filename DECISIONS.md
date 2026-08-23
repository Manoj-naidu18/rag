# Decisions

## 23 August 2026: date-aware policy answers

I kept retrieval, answer wording, and refusal in separate methods so the amendment can change without rewriting the command line. The assistant uses the date of the change for reporting rules, because Amendment No. 2026-01 §5.2 says those changes apply only when the change occurred on or after 1 March 2026. It uses the determination date for earnings, thresholds, and sanctions, following §1.2.3 and Amendment No. 2026-01 §5.1. When a question gives no date, it uses the current evaluation date in the brief, 23 August 2026.

I answer only topics for which I can name the controlling clauses. A question about an unlisted cost, such as childcare, is refused with a next step rather than answered from general benefits knowledge. Unknown questions are also refused. This is conservative: a false positive could give a resident the wrong expectation, while a caseworker can resolve a refusal with the manual or a supervisor.

The amendment is applied as an explicit rule instead of silently rewriting the source manual. That preserves the original text for audit and makes the transition visible in the citations. I did not add a language model or external knowledge source because neither is needed for this small fixed corpus and either would make the answer boundary harder to explain.
