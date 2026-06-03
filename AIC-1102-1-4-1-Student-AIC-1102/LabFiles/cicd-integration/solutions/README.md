# Solution Reference

Three worked workflows and a preToolUse hook.

## Workflows

- `.github/workflows/ci-with-diagnosis.yml` — the Core solution. Runs pytest; on failure, pipes output into Copilot CLI for a root-cause diagnosis saved as an artifact. Fails the job at the end so the status correctly reflects the test result.
- `.github/workflows/pr-quality.yml` — Challenge 1. Runs on every pull request; collects the diff, asks Copilot CLI for a structured review summary, posts it as a PR comment.
- `.github/workflows/ci-hardened.yml` — Challenge 2. The Core workflow with security hardening: pinned action SHAs (commented), minimum permissions, size-capped diff input, artifact sanitization step, and a `preToolUse` hook gating Copilot CLI's tool calls.

## Hook

- `hooks/pretooluse.py` — preToolUse hook designed for the pipeline context. Denies any shell tool call containing a dangerous pattern and allows a small, explicit safe subset.

## Using These Files

Copy individual workflows into your `.github/workflows/` directory one at a time. Do not enable all three simultaneously on the same branch during the lab — the Core workflow and the hardened workflow would both run, producing duplicate artifacts.

If your organization restricts which action SHAs can be used, update the comments next to each `uses:` line to the organization-approved SHA. The solution uses version tags (`@v4`) for readability; pin to SHAs for production.
