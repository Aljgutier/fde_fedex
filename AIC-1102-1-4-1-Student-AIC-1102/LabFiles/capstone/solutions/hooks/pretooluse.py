#!/usr/bin/env python3
"""preToolUse hook enforcing the Phase 4 deny list.

Contract:
    stdin:  JSON {"toolName": "...", "toolArgs": "<JSON-encoded string>"}
    stdout: JSON {"permissionDecision": "allow" | "deny",
                  "permissionDecisionReason": "..."}
    stderr: audit text (category + matched pattern)
    exit:   0 on any normal decision (including deny);
            non-zero only if the hook itself errored.
"""

import json
import re
import shlex
import sys
from urllib.parse import urlparse

# Categories from DENY_LIST.md. The pattern list is intentionally flat so
# the matched pattern is easy to report in the denial reason.
DENY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("recursive-delete", re.compile(r"\brm\b.*-r(?:f|ecursive)?\b")),
    ("permission-escalation", re.compile(r"\bchmod\b\s+(?:777|u\+s|\+s)\b")),
    ("remote-code-exec", re.compile(r"(?:curl|wget|fetch)\b.*\|\s*(?:sh|bash)")),
    ("fork-bomb", re.compile(r":\s*\(\s*\)\s*\{")),
    ("disk-primitive", re.compile(r"\b(?:mkfs|dd\s+if=/dev/)\b")),
    ("privilege-elevation", re.compile(r"\bsudo\b")),
    ("sensitive-path-write", re.compile(r">\s*/(?:etc|boot|var/log)\b")),
    ("raw-device-write", re.compile(r">\s*/dev/(?:sda|nvme|hda)")),
    ("git-destructive", re.compile(
        r"\bgit\s+(?:push\s+--force\b|reset\s+--hard\b|clean\s+-f[dx]?\b)"
    )),
]

NETWORK_ALLOWLIST = {
    "api.github.com",
    "raw.githubusercontent.com",
    "pypi.org",
    "files.pythonhosted.org",
}


def _is_shell_tool(tool_name: str) -> bool:
    return tool_name in {"shell", "run_command", "bash", "execute"}


def _is_fetch_tool(tool_name: str) -> bool:
    return tool_name in {"fetch_url", "http_get", "http_post"}


def _host_is_allowed(host: str) -> bool:
    if not host:
        return False
    host = host.lower()
    for allowed in NETWORK_ALLOWLIST:
        if host == allowed or host.endswith(f".{allowed}"):
            return True
    return False


def decide(tool_name: str, arguments: dict) -> tuple[bool, str]:
    if _is_shell_tool(tool_name):
        command = arguments.get("command", "") or ""
        for category, pattern in DENY_PATTERNS:
            if pattern.search(command):
                return False, f"{category} — {pattern.pattern}"
        return True, ""

    if _is_fetch_tool(tool_name):
        url = arguments.get("url", "") or ""
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False, f"scheme-not-allowed — {parsed.scheme}"
        if not _host_is_allowed(parsed.hostname or ""):
            return False, f"host-not-allowlisted — {parsed.hostname}"
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
