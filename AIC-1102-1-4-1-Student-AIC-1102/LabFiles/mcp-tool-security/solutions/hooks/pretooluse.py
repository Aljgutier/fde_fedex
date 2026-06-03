#!/usr/bin/env python3
"""preToolUse hook — full Core solution."""

import json
import os
import sys
from pathlib import Path


def _log_dir() -> Path:
    return Path(os.environ.get("LOG_DIR", "./sample_logs")).resolve()


def _rotate_log_file_denied(arguments: dict) -> tuple[bool, str]:
    filename = arguments.get("filename", "")
    if not isinstance(filename, str) or not filename:
        return True, "filename is required and must be a non-empty string"
    if "/" in filename or "\\" in filename or ".." in filename:
        return True, "filename must not contain path separators or traversal segments"
    if not filename.endswith(".log"):
        return True, "filename must end in .log"

    log_dir = _log_dir()
    target = (log_dir / filename).resolve()
    try:
        target.relative_to(log_dir)
    except ValueError:
        return True, "resolved target escapes the configured log directory"

    return False, ""


def decide(tool_name: str, arguments: dict) -> tuple[bool, str]:
    if tool_name.endswith("_force"):
        return False, "tool names ending in _force are blocked"
    if arguments.get("force") is True:
        return False, "force=true is not permitted through the hook"

    if tool_name == "rotate_log_file":
        denied, reason = _rotate_log_file_denied(arguments)
        if denied:
            return False, reason

    return True, ""


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
