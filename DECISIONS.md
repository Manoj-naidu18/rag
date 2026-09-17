# Decisions

## 23 August 2026: date-aware policy answers

I kept retrieval, answer wording, and refusal in separate methods so the amendment can change without rewriting the command line. The assistant uses the date of the change for reporting rules, because Amendment No. 2026-01 §5.2 says those changes apply only when the change occurred on or after 1 March 2026. It uses the determination date for earnings, thresholds, and sanctions, following §1.2.3 and Amendment No. 2026-01 §5.1. When a question gives no date, it uses the current evaluation date in the brief, 23 August 2026.

I answer only topics for which I can name the controlling clauses. A question about an unlisted cost, such as childcare, is refused with a next step rather than answered from general benefits knowledge. Unknown questions are also refused. This is conservative: a false positive could give a resident the wrong expectation, while a caseworker can resolve a refusal with the manual or a supervisor.

The amendment is applied as an explicit rule instead of silently rewriting the source manual. That preserves the original text for audit and makes the transition visible in the citations. I did not add a language model or external knowledge source because neither is needed for this small fixed corpus and either would make the answer boundary harder to explain.

## 17 September 2026: sharper refusal and visible contradiction

Two answer paths were weak, so I improved them without changing the structure or the retrieval/answer/refusal separation.

The full-time student question used to fall through to the generic refusal. It now has its own path that shows the reference trail: §1.4.6 defines the term only, §3.2.3 and §5.2.3 say full-time education is "addressed separately", and §7.1.3 points to §5.4 for the calculation - but §5.4 is about a care allowance, not students. Because the pointer leads to the wrong topic, the manual genuinely does not settle the question, and the case is sent to a supervisor. A refusal that shows why is more useful to a caseworker than "not enough information".

The reporting-deadline answer for a change before 1 March 2026 used to give 10 days as if settled. The manual actually contradicts itself: §4.3.2 says 10 days while §9.1.4 refers to "the 30 calendar days required under §4.3". The answer now surfaces both figures, names §4.3.2 as the operative rule, and flags the §9.1.4 conflict rather than hiding it. Amendment No. 2026-01 resolves the conflict to 14 days for changes on or after 1 March 2026, so that date still gives a single settled answer.

The answer/refusal boundary is unchanged in principle: I answer only where I can name the controlling clauses, I refuse where the manual does not settle the matter, and I now make a contradiction visible instead of choosing one side. The test set was extended from ten to twelve checks to cover these two cases.
