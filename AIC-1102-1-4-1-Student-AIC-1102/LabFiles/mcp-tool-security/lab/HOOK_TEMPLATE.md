# preToolUse Hook Contract

A preToolUse hook is a script that runs *before* the agent executes a tool call. It inspects the tool name and arguments and decides whether the call proceeds. Hooks are the mechanism that makes "require approval for high-risk tools" enforceable instead of polite.

This document describes the hook contract used by the lab's starter hook in `hooks/pretooluse.py`. The exact wiring for GitHub Copilot CLI and the cloud agent may shift between releases; check the current Copilot documentation if a field name here does not match your installed version.

## Input

The hook reads JSON on stdin. The schema is:

```json
{
  "toolName": "rotate_log_file",
  "toolArgs": "{\"filename\":\"app.log\"}"
}
```

Notes:

- `toolName` is a plain string — the fully qualified tool name (server and tool).
- `toolArgs` is a **string containing a JSON document**, not a nested JSON object. Parse it with a second `json.loads` call to access the individual arguments.

## Output

- **stdout**: a single JSON document expressing the decision:

  ```json
  { "permissionDecision": "allow" }
  ```

  ```json
  { "permissionDecision": "deny", "permissionDecisionReason": "human-readable reason" }
  ```

  `permissionDecision` is required; `permissionDecisionReason` is optional but strongly recommended for `deny` so the agent can explain the refusal to the user.

- **stderr**: free-form audit output. Anything printed here is attached to the tool call in the session log but does not drive the decision.

- **Exit code**: `0` on any normal completion, including `deny`. Non-zero exit codes indicate the hook itself errored (malformed input, unhandled exception). Treat non-zero as a hook failure, not a denial.

## What the Hook Should Do

### Always

- Be fast. The hook runs synchronously on every tool call; treat anything above ~100ms as a bug.
- Be deterministic. Given the same input, always return the same decision. Random denials destroy the agent's ability to recover.
- Fail closed. If the hook cannot parse the input, emit `{"permissionDecision":"deny","permissionDecisionReason":"malformed hook input"}` and exit 0.

### Never

- Make network calls from the hook itself. The hook is a local checkpoint; network I/O belongs in a tool, not a gatekeeper.
- Mutate the repository or the filesystem. A hook that writes files is not a checkpoint; it is a second tool running behind the agent's back.
- Log the full arguments of every tool call to disk. Some tool arguments contain sensitive data (file paths, request bodies). Log only what you need for audit.

## Wiring

Hooks register via `.github/hooks/hooks.json` (JSON, not YAML). The file sits in `.github/hooks/` — not `.github/copilot/` — and uses a `hooks` array of match rules:

```json
{
  "hooks": [
    {
      "matchers": [{ "type": "tool_use", "toolName": "rotate_log_file" }],
      "preToolUse": {
        "command": "python",
        "args": ["hooks/pretooluse.py"]
      }
    }
  ]
}
```

Multiple matcher entries can appear; the first match wins. Omitting a matcher entry makes the hook run for every tool call.

## Testing Hooks Standalone

Because the hook reads JSON on stdin and writes a JSON decision on stdout, you can test it without the agent:

```bash
echo '{"toolName":"rotate_log_file","toolArgs":"{\"filename\":\"../etc/passwd\"}"}' \
  | python hooks/pretooluse.py
echo "exit: $?"
```

Expected stdout after implementing the denial rules:

```json
{"permissionDecision":"deny","permissionDecisionReason":"filename contains path separator"}
```

Expected exit code: `0`.
