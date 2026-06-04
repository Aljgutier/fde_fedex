"""MCP server exposing a network fetcher tool — STUB for Challenge 1.

Fill in the allowlist and the domain check in `http_get` below. The
goal is to enforce the allowlist at the TOOL level, not rely on
Copilot's self-restraint.
"""

import os
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("net-tools")


# TODO: define the allowlist. Keep it short — two or three domains.
# Environment override (comma-separated) is a reasonable affordance.
ALLOWED_DOMAINS: set[str] = set()


def _is_allowed(url: str) -> bool:
    """Return True iff the URL's host (or a parent domain) is in ALLOWED_DOMAINS.

    TODO: implement. Cases to handle:
      - Exact host match (e.g. "api.example.com" in ALLOWED_DOMAINS)
      - Subdomain match (host "docs.example.com" is allowed if
        "example.com" is in ALLOWED_DOMAINS)
      - Scheme enforcement (only http and https; reject file://, etc.)
    """
    raise NotImplementedError


@mcp.tool()
def http_get(url: str, timeout_seconds: int = 10) -> dict:
    """Fetch ``url`` via HTTP GET and return the response body and status.

    Network operation. Only URLs whose host is on the allowlist will
    succeed; any other URL is rejected at the tool level before the
    request is issued.

    Args:
        url: Absolute URL to fetch. Must be http or https.
        timeout_seconds: Request timeout. Defaults to 10, maximum 30.

    Returns:
        A dict with keys `status`, `body` (truncated to 8 KiB), and
        `url_final` (the URL actually fetched, accounting for redirects).
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
