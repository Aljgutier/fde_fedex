# 2 Lab Notes Code Review and Refinement

You will review a small Python order-processing module with GitHub Copilot. 

The code runs and the tests pass, but it hides real problems: duplicated constants across files, a quietly wrong calculation, inconsistent naming, and functions without documentation.

You have inherited an order-processing module that was written in a hurry. The tests pass, the app runs, and nobody has complained — but it has been sitting in the backlog as "technical debt, unknown severity" for six months.

Before the next billing release you want to do a structured code review, using Copilot as your reviewer, to identify which issues are real and which are cosmetic. 

The lab mirrors the kind of inherited-codebase triage that happens every time a team takes on a new service.

The starter contains at least one of each of the following categories:
* A latent bug that produces the wrong answer without raising an error
* A cross-file inconsistency only visible when you look at more than one file
* Common Python anti-patterns (mutable default argument, bare except, dead code)
* Missing documentation

# Setup
* uv venv
* pip install packages
* pytest ... 3 passed testws


# Baseline Fixes
* open orders.py
* highlieht process_order.py


**Fix a method ... invoke /fix**
* prompt ... Agent mode
```
/fix Review this function for correctness and code quality.
List each issue you find with a one-sentence rationale.
```

* In REVIEW_NOTES.md, under a heading ## /fix baseline (orders.py), list the issues Copilot surfaced. Do not change any code yet.

**Codebase review**

prompt
```
#codebase Review this repository for correctness, consistency,
code quality, and documentation. Group findings by file.
Include cross-file issues as their own section.
```

**Fill Documentation Gaps with /doc**

```
/doc Write a concise docstring describing purpose, parameters,
and return value.
```

Accept Modify or Reject Changes


**Refinement Prompt**
```
Your previous suggestion to <X> was correct in intent, but
it <specific problem>. Rewrite the change so that <constraint>.
```

**Run Pytest**
```
pytest -v
```