"""MCP server exposing a network fetcher tool with a domain allowlist."""

import os
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "net-tools",
    instructions=(
        "Network fetcher tools. Requests are restricted to a domain "
        "allowlist enforced in the tool. Any request to a non-allowlisted "
        "host is rejected before the HTTP call is issued."
    ),
)


def _default_allowlist() -> set[str]:
    return {"api.github.com", "raw.githubusercontent.com"}


def _configured_allowlist() -> set[str]:
    override = os.environ.get("NET_TOOLS_ALLOWLIST")
    if override:
        return {item.strip().lower() for item in override.split(",") if item.strip()}
    return _default_allowlist()


ALLOWED_DOMAINS = _configured_allowlist()


def _host_is_allowed(host: str) -> bool:
    if not host:
        return False
    host = host.lower()
    for allowed in ALLOWED_DOMAINS:
        if host == allowed or host.endswith(f".{allowed}"):
            return True
    return False


def _is_allowed(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    return _host_is_allowed(parsed.hostname or "")


@mcp.tool()
def http_get(url: str, timeout_seconds: int = 10) -> dict:
    """Fetch ``url`` via HTTP GET and return the response body and status.

    Network operation. Only URLs whose host matches the allowlist
    (currently ``api.github.com`` and ``raw.githubusercontent.com``,
    overridable via ``NET_TOOLS_ALLOWLIST``) will be fetched. Any other
    URL is rejected at the tool level.

    Args:
        url: Absolute URL. Must use http or https.
        timeout_seconds: Request timeout. Defaults to 10, capped at 30.

    Returns:
        A dict with `status`, `body` (truncated to 8 KiB), and
        `url_final`, or a dict with `error` and `url` on rejection.
    """
    if not _is_allowed(url):
        return {"error": "url not on allowlist", "url": url}

    timeout = min(max(1, timeout_seconds), 30)
    req = Request(url, headers={"User-Agent": "net-tools/0.1"})
    with urlopen(req, timeout=timeout) as resp:
        body = resp.read(8 * 1024).decode("utf-8", errors="replace")
        return {
            "status": resp.status,
            "body": body,
            "url_final": resp.url,
        }


if __name__ == "__main__":
    mcp.run()
