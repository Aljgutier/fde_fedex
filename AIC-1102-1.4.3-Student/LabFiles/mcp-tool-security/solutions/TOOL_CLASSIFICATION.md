# Tool Classification — Reference Answer

One possible classification for the five tools in this lab. Reasonable people may draw the line slightly differently on `http_get` depending on their stance toward allowlists; the important part is the reasoning chain, not the label.

| Tool                 | Server     | Classification | Reasoning |
|----------------------|------------|----------------|-----------|
| `list_logs`          | log-tools  | Safe           | Read-only enumeration of a bounded directory. No mutation. No credentials. The tool resolves filenames against a configured `LOG_DIR`; it cannot be coerced into listing arbitrary paths. |
| `search_logs`        | log-tools  | Safe           | Read-only search scoped to `LOG_DIR`. Even with a pathological regex, the worst case is a slow response — no mutation, no exfiltration path. The `limit` parameter bounds output size. |
| `count_logs_by_level`| log-tools  | Safe           | Read-only aggregation over `LOG_DIR`. Returns counts only, no line content. Smallest blast radius of all the tools. |
| `rotate_log_file`    | log-tools  | High-Risk      | Write operation. Moves files and creates empty replacements. A malformed `filename` (traversal, non-`.log`, path separator) could target files outside `LOG_DIR`. Irreversible without backup handling. Requires user confirmation AND preToolUse hook enforcement for filename safety. |
| `http_get`           | net-tools  | High-Risk      | Network access. Even with the allowlist, the tool issues external requests and returns response bodies that may contain untrusted content the agent then reasons over (prompt injection surface). The allowlist must be enforced at the tool level; treating "allowlist enforced" as a reason to downgrade to Safe would be wrong — the allowlist prevents network misuse, not the risks inherent to any external data entering the agent's context. |

## Where the Decision Rule Landed

- Three Safe tools: run without confirmation in Agent Mode.
- Two High-Risk tools: require explicit confirmation on every call. `rotate_log_file` additionally has a preToolUse hook for argument-level checks that a confirmation modal cannot enforce.

## Edge Cases Worth Noting

- `search_logs` is Safe *today* because the implementation is bounded to `LOG_DIR` and has a `limit` parameter. If either of those changed — if `LOG_DIR` became user-provided per call, or if `limit` were removed — it would move to High-Risk. Classification is a property of the current implementation, not the tool name.
- `http_get` with an allowlist is still High-Risk because external data entering the agent's context is a risk in itself (prompt injection, data exfiltration through follow-up tool calls). An allowlist controls *which* external data is admitted; it does not eliminate the category.
- `count_logs_by_level` is the only tool where even a much-looser implementation would still be Safe — counts of levels are sufficiently abstracted that even unbounded scope would not leak meaningful content. This is rare.
