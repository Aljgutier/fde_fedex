# Tool Classification

Fill in the table below during Core Step 1. One row per tool from `log_tools/server.py` and `net_tools/server.py`. Use the criteria section below the table to justify each decision.

## Classification Table

| Tool                 | Server     | Classification   | Reasoning |
|----------------------|------------|------------------|-----------|
| `list_logs`          | log-tools  | _fill in_        | _fill in_ |
| `search_logs`        | log-tools  | _fill in_        | _fill in_ |
| `count_logs_by_level`| log-tools  | _fill in_        | _fill in_ |
| `rotate_log_file`    | log-tools  | _fill in_        | _fill in_ |
| `http_get`           | net-tools  | _fill in_        | _fill in_ |

## Classification Criteria

### Safe (no confirmation required)

A tool is Safe if *all* of the following are true:

- Read-only. The tool does not modify any persistent state — no file writes, no database mutations, no API calls with side effects.
- Reversible. Even if the tool returns an unexpected result, nothing has changed in the environment that would need to be rolled back.
- Low blast radius. The data the tool touches is scoped: a log directory, a specific subtree, or a configured resource. The tool cannot be coerced into reading arbitrary paths on the machine.
- No credential or secret access. The tool does not read environment variables, secret stores, or files that typically contain secrets (even if the requested operation would not directly surface them).
- No network access. Or, if network access is required, the tool is locked down to an allowlist enforced in the tool itself (not in the agent's prompt).

### High-Risk (confirmation required)

A tool is High-Risk if *any* of the following are true:

- It modifies persistent state (writes a file, mutates a database, calls a state-changing API).
- It can affect resources outside the tool's intended scope (path traversal risk, unbounded queries, unbounded fan-out).
- It accesses credentials, environment variables, or secret stores.
- It makes arbitrary network calls. "Arbitrary" here means: the target domain is a function of the tool argument, not the tool implementation.
- It runs shell commands, invokes executables, or manipulates processes.

## Decision Rule

If a tool lands in Safe, it runs without confirmation in Agent Mode.

If a tool lands in High-Risk, it requires explicit user approval on every call, *and* a preToolUse hook should enforce the specific denial rules you cannot express through "approve / deny" alone (path traversal, invalid filenames, destructive flags).

Safe and High-Risk are not opinions — they determine the configuration you apply in the next steps. Get the classification wrong and either the agent stops for every harmless read, or it makes a destructive call without a checkpoint.
