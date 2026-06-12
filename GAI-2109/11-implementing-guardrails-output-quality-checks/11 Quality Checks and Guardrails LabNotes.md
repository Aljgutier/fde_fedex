# 11 Guardrails and Quality Checks


Production agents need guardrails—automated checks that prevent harmful, inappropriate, or low-quality outputs. Without guardrails, agents can:

* Generate offensive or dangerous content
* Leak sensitive information
* Produce factually incorrect responses
* Violate regulatory requirements


**Guardrail Categories**

Input Guardrails

* Topic restrictions (forbidden subjects)
* Jailbreak prevention (prompt injection)
* Rate limiting and abuse detection

Output Guardrails

* Content m
* PII detection and redaction
* Factual accuracy checking
* Quality thresholds (length, completeness)


You’re deploying a customer service agent for a financial services company. Regulatory requirements mandate:

* No disclosure of account details without verification
* Detection and redaction of Social Security numbers
* Rejection of queries about competitors' products
* Professional, safe language only


**Problem Statement**
* Objective: Wire three pre-built guardrail modules (input validation, output validation, PII detection) into a financial services support agent so that unsafe queries are blocked, policy violations fail closed, and PII is redacted from responses.

* Expected Outcome: A working handle_query_with_guardrails() function that runs each user query through a four-stage pipeline (input check → agent call → output check → PII redaction) and returns a structured result dictionary noting which guardrails fired.

