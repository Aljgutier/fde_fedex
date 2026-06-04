# Copilot CLI in GitHub Actions — Reference

The snippets in this document show the pattern pieces you will compose into a complete workflow in the Core phase. They are reference — not cut-and-paste fragments. You are expected to adapt them to the specific step order and conditions in your workflow.

The exact command names and flag syntax for Copilot CLI may shift between versions; check `copilot --help` on your installed version if any flag here does not behave as described.

## Install Copilot CLI in a Runner

```yaml
- name: Install Copilot CLI
  run: npm install -g @github/copilot@latest
```

Copilot CLI is distributed as an npm package and installs in seconds on a GitHub-hosted runner. Installation itself does not authenticate — that step is separate.

## Authenticate With an Environment Variable

Copilot CLI reads its token from an environment variable. The resolution order as of April 2026 is:

1. `COPILOT_GITHUB_TOKEN` — the Copilot-specific override
2. `GH_TOKEN` — the standard GitHub CLI token
3. `GITHUB_TOKEN` — the Actions-default token

The first one set wins. In a workflow, pass the secret into the step that invokes `copilot`:

```yaml
- name: Diagnose failures
  if: steps.pytest.outcome == 'failure'
  run: |
    cat pytest-output.log | copilot -p "Analyze the pytest output..." > diagnosis.md
  env:
    COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}
```

Notes:

- The token comes from a repository secret. Never hardcode one.
- There is **no** `GITHUB_ASKPASS` helper-script step — Copilot CLI does not go through the git credential helper path. Older community workflows that write an askpass shim are carrying over a pattern from a different tool.
- If you need the token available to several steps in the same job, pass `env:` on each step rather than exporting globally — that keeps the secret scoped to the steps that actually need it.

## Invoke Copilot CLI Non-Interactively

The `-p` flag puts Copilot CLI into pipeline mode: reads input on stdin, writes output on stdout, no confirmation prompts.

```yaml
- name: Diagnose failures
  run: |
    cat pytest-output.log | copilot -p "Analyze the pytest output..." > diagnosis.md
  env:
    COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}
```

Prompt design matters more here than in Chat. Structured output prompts ("Produce the output as markdown with sections ...") are more reliable than open-ended prompts in a pipeline.

## Conditional Execution on Test Failure

Use `continue-on-error: true` on the test step so subsequent steps can run. Then gate each diagnostic step on the outcome.

```yaml
- name: Run tests
  id: pytest
  continue-on-error: true
  run: pytest --tb=short 2>&1 | tee pytest-output.log

- name: Diagnose (only on failure)
  if: steps.pytest.outcome == 'failure'
  run: |
    cat pytest-output.log | copilot -p "..." > diagnosis.md

- name: Upload diagnosis artifact
  if: steps.pytest.outcome == 'failure'
  uses: actions/upload-artifact@v7
  with:
    name: copilot-diagnosis
    path: diagnosis.md

- name: Fail the job if tests failed
  if: steps.pytest.outcome == 'failure'
  run: exit 1
```

Without the explicit `exit 1` at the end, the job goes green despite failing tests — not what you want.

## Post a PR Comment With the GitHub CLI

```yaml
- name: Post summary as PR comment
  if: github.event_name == 'pull_request'
  run: gh pr comment "$PR_NUMBER" --body-file quality-summary.md
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    PR_NUMBER: ${{ github.event.pull_request.number }}
```

`gh` is pre-installed. `GH_TOKEN` (not `GITHUB_TOKEN` — the name is unique to `gh`) selects the token `gh` authenticates with.

## Collect the PR Diff

```yaml
- uses: actions/checkout@v6
  with:
    fetch-depth: 0  # need history to compute the diff base

- name: Collect PR diff
  run: |
    git diff origin/${{ github.base_ref }}...HEAD --unified=3 > pr.diff
```

Note `fetch-depth: 0`. Without it, the runner has only the tip of the branch and `git diff` against the base ref fails.

## Minimum Permissions

A workflow that only reads code and writes PR comments should declare minimum permissions explicitly:

```yaml
permissions:
  contents: read
  pull-requests: write
```

`GITHUB_TOKEN` defaults are broader than necessary. Declare the minimum.
