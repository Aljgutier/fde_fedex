# MCP Access Policy

This document defines which MCP tool categories are permitted for autonomous agent use in this repository, which require human approval via a `preToolUse` hook, and which are denied outright.

## Scope

Applies to every MCP server registered for use with the cloud agent, Agent Mode, or Copilot CLI when those agents operate against this repository. Does not apply to interactive Chat sessions where the user confirms each call.

## Policy Categories

### Permitted (no approval required)

These tool categories run without a confirmation prompt. Their blast radius is bounded by construction: read-only, scope-limited, or producing derivatives the agent cannot act on without a further tool call.

- Repository read operations: listing files, reading file contents, grepping in the working directory.
- Repository search via the Copilot workspace index.
- Issue and pull-request *read* on the GitHub MCP server: list, view, read comments.
- Test execution (`pytest`) and its output parsing.
- Static analysis that produces reports only (linters, type checkers, audit scripts).
- Read-only queries against the project's MCP log-tools server or equivalent read-only servers.

### Requires Approval (hook-gated with human confirmation)

These categories require an approval prompt *and* pass a `preToolUse` hook check before executing. The hook enforces argument-level rules that a yes-or-no modal cannot express (path traversal, forbidden flags, out-of-scope targets).

- Issue and pull-request *write* on the GitHub MCP server: create issue, comment, open PR, request review. Hook check: the target repository is this one and nothing else.
- File writes inside the repository working directory. Hook check: path is inside the workspace and not inside `.github/`, `DENY_LIST.md`, `AGENTS.md`, or under `docs/policy/`.
- Git operations: branch creation, commit, push of a non-destructive change. Hook check: branch name matches a feature-branch pattern, not `main` or `release/*`.
- Outbound HTTP fetches to the repository's pre-approved allowlist (`api.github.com`, `pypi.org`, `files.pythonhosted.org`, `raw.githubusercontent.com`). Hook check: URL host matches the allowlist; scheme is `https`.
- Package installs from PyPI via `pip install`. Hook check: the package name is in `requirements.txt` or already installed; the version is pinned.

### Denied (not available to autonomous agents)

These categories are not exposed to agents that run without continuous human supervision. A human operator must perform the action directly.

- **Direct production database writes.** No MCP server with credentials to a production database is registered for autonomous use. Schema migrations and data patches are human-run.
- **Secret store access.** No tool may read or write from a secret manager (Vault, AWS Secrets Manager, 1Password). Credentials reach agents only via environment variables set at job start, never fetched at runtime.
- **Deployment triggers.** No tool may start a production deployment (`helm upgrade`, `kubectl apply` against a production context, CD pipeline manual triggers). The cloud agent opens PRs; humans merge; humans deploy.
- **Destructive git operations.** `push --force`, `reset --hard`, `branch -D`, `tag --delete`, repository deletion. Covered by the deny-list hook; repeated here because the policy stance is "deny", not "hook with careful rules".
- **Privilege escalation.** `sudo`, `su`, any mechanism to run as a different OS user.
- **Unrestricted network access.** Any outbound HTTP to a host outside the approved allowlist. No `curl | sh`, no `wget` to arbitrary domains.
- **Recursive filesystem deletion** outside a designated temp directory.
- **System-level package installs** (`apt`, `yum`, `brew`). Runtime images are prebuilt; agents do not reshape the runtime.

## Enforcement Layers

1. **Tool schema** — tools that would appear in the Denied category are not registered in the agent's MCP server set. Absence is the first defense.
2. **`preToolUse` hook** — `hooks/pretooluse.py` blocks the shell and fetch patterns that map to Denied categories even if a tool permits them structurally.
3. **User confirmation** — Requires-Approval categories prompt the human operator on every call. `alwaysAllow` is forbidden for any tool in this category.
4. **GitHub branch protection** — `main` is protected; no agent can merge. Human review is the final gate for anything that ships.

## Residual Risks

Technical controls cover most categories but not all. These remain human-process concerns:

- **Prompt injection via read inputs** — an agent that reads a file or webpage containing adversarial instructions may attempt tool calls based on those instructions. The hook limits damage; human review of agent session logs is required when the agent processes any untrusted content.
- **Token exfiltration** — a compromised agent could attempt to read credentials from the environment and exfiltrate them via an allowlisted channel (a PR comment, a write to an allowed path). Mitigation: short-lived, narrowly-scoped tokens; no long-lived credentials in agent runners.
- **Scope drift** — over time, "temporary" approvals in `toolPermissions` accrete into permanent trust. Mitigation: quarterly review of `toolPermissions` in `.vscode/settings.json` and this policy document.

## Review Cadence

This document is reviewed at least quarterly, and whenever:

- A new MCP server is registered for autonomous use
- A new category of tool is added to any existing server
- An incident reveals a gap in the policy
- Copilot introduces a new tool surface (new hook events, new agent modes)

Approvers: the security-engineering owner and the platform-engineering owner. Changes require at least one approval from each.

## Change Log

- **Initial policy** — capstone reference version. Derived from the labs in the Foundations of Coding Agents with GitHub Copilot course.
