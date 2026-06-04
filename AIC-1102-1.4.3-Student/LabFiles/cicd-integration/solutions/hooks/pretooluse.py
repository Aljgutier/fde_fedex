#!/usr/bin/env python3
"""preToolUse hook for Copilot CLI in a CI/CD pipeline.

Denies tool calls whose arguments contain dangerous shell patterns, and
restricts the shell tool to an explicit allowlist of safe read-only
commands. Anything else is denied with a reason.

Contract:
    stdin:  JSON {"toolName": "...", "toolArgs": "<JSON-encoded string>"}
    stdout: JSON {"permissionDecision": "allow" | "deny",
                  "permissionDecisionReason": "..."}
    stderr: free-form audit text (optional)
    exit:   0 on any normal decision (including deny);
            non-zero only if the hook itself errored.
"""

import json
import re
import shlex
import sys


DANGEROUS_PATTERNS = [
    re.compile(r"\brm\b.*-rf\b"),
    re.compile(r"\bchmod\b\s+(?:777|u\+x)\b"),
    re.compile(r"\bcurl\b.*\|\s*(?:sh|bash)"),
    re.compile(r"\bwget\b.*\|\s*(?:sh|bash)"),
    re.compile(r":\s*\(\s*\)\s*\{"),
    re.compile(r"\b(?:mkfs|dd\s+if=/dev)\b"),
    re.compile(r">\s*/dev/(?:sda|nvme|hda)"),
    re.compile(r"\bsudo\b"),
]


SAFE_SHELL_COMMANDS = {
    "cat", "grep", "awk", "sed", "head", "tail", "wc", "sort", "uniq",
    "cut", "tr", "find", "ls", "pwd", "echo", "jq", "git",
    "pytest", "python", "python3",
}


def _is_shell_tool(tool_name: str) -> bool:
    return tool_name in {"shell", "run_command", "bash", "execute"}


def _shell_command_head(command: str) -> str | None:
    try:
        parts = shlex.split(command)
    except ValueError:
        return None
    return parts[0] if parts else None


def decide(tool_name: str, arguments: dict) -> tuple[bool, str]:
    if _is_shell_tool(tool_name):
        command = arguments.get("command", "") or ""
        for pattern in DANGEROUS_PATTERNS:
            if pattern.search(command):
                return False, f"dangerous pattern matched: {pattern.pattern}"
        head = _shell_command_head(command)
        if head is None:
            return False, "could not parse shell command"
        if head not in SAFE_SHELL_COMMANDS:
            return False, f"shell command not in safe allowlist: {head}"
        return True, ""

    if tool_name in {"write_file", "edit_file", "delete_file", "apply_diff"}:
        return False, f"write-capable tool not permitted in pipeline context: {tool_name}"

    if tool_name in {"fetch_url", "http_get", "http_post"}:
        url = arguments.get("url", "") or ""
        if not url.startswith(("https://api.github.com", "https://raw.githubusercontent.com")):
            return False, f"network fetch outside allowlist: {url}"
        return True, ""

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
