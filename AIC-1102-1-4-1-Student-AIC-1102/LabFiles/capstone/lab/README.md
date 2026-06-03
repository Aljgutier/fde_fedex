# Capstone — Composability and Extensibility

The final lab of the course. Four phases synthesize the techniques from the previous twelve: shell composability (Lab 12), scripted automation (Lab 12), the full custom configuration stack (Lab 5), and orchestrated cloud agents with guardrails (Labs 6, 7, 8).

## Layout

```
.
├── src/
│   ├── auth.py        # login/logout workflow
│   ├── session.py     # session token store
│   ├── users.py       # user record store
│   └── utils.py       # password hashing, email normalization, token generation
├── tests/
│   ├── test_auth.py
│   └── test_users.py
├── FEATURE_BRIEF.md   # password hashing utility specification (Phase 4 target)
├── DENY_LIST.md       # terminal commands the Phase 4 hook must block
├── requirements.txt
└── solutions/
    ├── reports/
    │   ├── security_audit.md    # Phase 1 example output
    │   └── test_diagnosis.md    # Phase 2 example output
    ├── scripts/
    │   └── diagnose.sh          # Phase 2 reference script
    ├── .github/
    │   ├── copilot-instructions.md
    │   ├── instructions/
    │   │   └── audit.instructions.md
    │   └── skills/
    │       ├── developer/SKILL.md
    │       └── reviewer/SKILL.md
    ├── AGENTS.md
    ├── hooks/
    │   └── pretooluse.py        # Phase 4 deny-list hook
    ├── src/password.py          # Phase 4 reference implementation
    ├── tests/test_password.py
    ├── PULL_REQUEST_TEMPLATE.md # Challenge 1
    └── docs/mcp_security.md     # Challenge 2
```

## Starting State

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

You should see a mix of passing and failing tests. That is the Phase 2 diagnostic target. Copy the bug inventory from `pytest --tb=short` to establish the baseline before continuing.

## What to Expect

The source code has deliberately planted `TODO` and `FIXME` comments with a mix of security concerns (MD5 hashing, timing-attack-vulnerable comparison, short session tokens) and ordinary code-quality notes. The Phase 1 audit will surface them; the Phase 3 configuration stack will shape how Copilot responds to them; the Phase 4 cloud agent will build the replacement for the weakest of them.

## Scope

This lab requires a GitHub repository to exercise the cloud agent and pull request workflows. Push this directory to a private repository before Phase 4 begins.
