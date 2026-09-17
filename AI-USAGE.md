# AI usage

I used AI coding assistants - ChatGPT and GitHub Copilot - to help outline the file structure, draft small Python functions, and review the test questions.

I supplied the policy manual and amendment as the only policy sources. I checked the date rules, clause numbers, refusal behavior, and test outputs against those files myself. The assistant does not call an AI service at runtime; it uses Python's standard library and a small set of explicit policy topics.

The final code was kept deliberately direct so another developer can explain each answer path during review. I remain responsible for the design choices, the answer/refusal boundary, and every clause the assistant cites.
