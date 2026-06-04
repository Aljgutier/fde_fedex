#!/usr/bin/env python3
"""preToolUse hook — STUB.

Contract:
    stdin:  JSON {"toolName": "<string>", "toolArgs": "<JSON-encoded string>"}
    stdout: JSON {"permissionDecision": "allow"}
            or   {"permissionDecision": "deny",
                  "permissionDecisionReason": "<string>"}
    stderr: free-form audit text (optional)
    exit:   0 on any normal decision (including deny);
            non-zero only if the hook itself errored.

Your job: fill in the denial rules for ``rotate_log_file``. Deny the call
if any of the following are true about the ``filename`` argument:

  1. The filename contains a path separator (``/`` or ``\\``) or ``..``
     — a rotate call should only target a file inside the log directory,
     not a traversal target.
  2. The filename does not end in ``.log``.
  3. The filename resolves to a file outside the log directory after
     joining with the environment variable ``LOG_DIR``.

Also deny any tool call whose ``toolName`` ends with ``_force`` or where
the arguments include a boolean ``force: true`` — these are the
"destructive override" patterns you were asked to block.

Approve every other call silently.
"""

import json
import sys


def decide(tool_name: str, arguments: dict) -> tuple[bool, str]:
    """Return (allow, reason).

    TODO: implement the denial rules from the docstring above.
    Return (True, "") to allow; return (False, "<reason>") to deny.
    """
    raise NotImplementedError


def _emit(decision: str, reason: str = "") -> None:
    payload = {"permissionDecision": decision}
    if reason:
        payload["permissionDecisionReason"] = reason
    json.dump(payload, sys.stdout)
    sys.stdout.write("\n")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"hook: malformed input: {exc}", file=sys.stderr)
        _emit("deny", f"malformed hook input: {exc}")
        return 0

    tool_name = payload.get("toolName", "")
    raw_args = payload.get("toolArgs", "{}") or "{}"
    try:
        arguments = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
    except json.JSONDecodeError as exc:
        print(f"hook: malformed toolArgs: {exc}", file=sys.stderr)
        _emit("deny", f"malformed toolArgs: {exc}")
        return 0

    if not isinstance(arguments, dict):
        arguments = {}

    allow, reason = decide(tool_name, arguments)
    if not allow:
        print(f"hook: denied {tool_name}: {reason}", file=sys.stderr)
        _emit("deny", reason)
        return 0

    _emit("allow")
    return 0


if __name__ == "__main__":
    sys.exit(main())
