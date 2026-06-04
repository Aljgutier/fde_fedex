# CI/CD Integration with Copilot CLI

A small Python stats library with a basic GitHub Actions workflow that runs `pytest`. In this lab you will extend the workflow to run Copilot CLI in non-interactive mode for three purposes: diagnosing test failures, producing PR-level code quality summaries, and running inside a hardened pipeline with a preToolUse hook.

## Layout

```
.
├── src/
│   ├── __init__.py
│   └── stats.py
├── tests/
│   └── test_stats.py
├── .github/
│   └── workflows/
│       └── ci.yml               # basic pytest workflow — the starter
├── BUG_TRIGGER.md               # how to introduce a failing test for the Core demo
├── WORKFLOW_REFERENCE.md        # explanation of Copilot CLI pipeline patterns
├── requirements.txt
└── solutions/
    ├── .github/workflows/
    │   ├── ci-with-diagnosis.yml
    │   ├── pr-quality.yml
    │   └── ci-hardened.yml
    ├── hooks/
    │   └── pretooluse.py
    └── README.md
```

## Setup

This lab requires a GitHub repository with Actions enabled. You will push the starter to your own fork and exercise the workflow by triggering runs in the GitHub UI.

Local setup to sanity-check the code before pushing:

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

All starter tests should pass.

## What You Need on GitHub

- A repository with Actions enabled
- A repository secret named `COPILOT_GITHUB_TOKEN` containing a PAT or fine-grained token with appropriate scopes for Copilot CLI authentication (Copilot CLI reads `COPILOT_GITHUB_TOKEN` first, then falls back to `GH_TOKEN`, then `GITHUB_TOKEN`)
- The GitHub CLI (`gh`) is pre-installed on Actions runners by default

See `WORKFLOW_REFERENCE.md` for the specific snippets you will add to the workflow.
