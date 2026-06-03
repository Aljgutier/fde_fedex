"""MCP server exposing log tools. Complete server carried over from the
MCP Tool Design lab — the schema is stable here; security configuration
is the focus of this lab.
"""

import os
from typing import Literal

from mcp.server.fastmcp import FastMCP

from log_tools.reader import count_by_level, list_log_files, rotate_log, search

LOG_DIR = os.environ.get("LOG_DIR", "./sample_logs")

mcp = FastMCP("log-tools")


@mcp.tool()
def list_logs() -> list[str]:
    """List the log files available in the configured log directory.

    Read-only. Use this tool when the user asks which log files exist.

    Returns:
        A list of log filenames (relative to the log directory).
    """
    return list_log_files(LOG_DIR)


@mcp.tool()
def search_logs(
    pattern: str,
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] | None = None,
    limit: int = 100,
) -> list[dict]:
    """Search log messages for lines matching a regex.

    Read-only. Use this tool when the user asks to find specific log
    lines by text content.

    Args:
        pattern: Regex pattern matched against each log message.
        level: Optional log level filter.
        limit: Maximum number of results to return.

    Returns:
        A list of dicts with file, line_number, timestamp, level, message.
    """
    return search(LOG_DIR, pattern, level, limit)


@mcp.tool()
def count_logs_by_level() -> dict:
    """Return the number of log entries at each level across all log files.

    Read-only.

    Returns:
        A dict mapping DEBUG, INFO, WARNING, ERROR to counts.
    """
    return count_by_level(LOG_DIR)


@mcp.tool()
def rotate_log_file(filename: str) -> dict:
    """Archive a log file and create a new empty one in its place.

    WRITE operation. Modifies the filesystem. Use this only when the user
    explicitly asks to rotate, archive, or truncate a log.

    Args:
        filename: Name of the log file to rotate (relative to log dir).

    Returns:
        A dict with `archived_as` and `original`.
    """
    return rotate_log(LOG_DIR, filename)


if __name__ == "__main__":
    mcp.run()
