"""MCP server for local log reading tools.

Fill in the stub tools marked TODO below. Refer to SCHEMA_TEMPLATES.md
for the expected schema shapes, and compare your tool descriptions
against the GitHub MCP server's tool descriptions as a quality benchmark.
"""

import os

from mcp.server.fastmcp import FastMCP

from log_tools.reader import (
    count_by_level,
    list_log_files,
    rotate_log,
    search,
)

LOG_DIR = os.environ.get("LOG_DIR", "./sample_logs")

mcp = FastMCP("log-tools")


@mcp.tool()
def list_logs() -> list[str]:
    """List the log files available in the configured log directory.

    Use this tool when the user asks which log files exist, or before
    calling a tool that requires a specific filename and the filename
    has not yet been established.

    Returns:
        A list of log filenames (relative to the log directory).
    """
    return list_log_files(LOG_DIR)


# TODO: Implement `search_logs`.
#
# The tool should:
#   - Take a regex pattern and search log messages for matches
#   - Accept an optional `level` filter (DEBUG, INFO, WARNING, ERROR)
#   - Accept an optional `limit` on the number of results (default 100)
#   - Return a list of matching entries with file, line_number, timestamp,
#     level, and message fields
#
# Write a description that tells Copilot:
#   - When to use this tool (finding specific log lines by content)
#   - When NOT to use this tool (counting, listing files, or non-log data)
#   - What each argument means and what values are valid
#
# Use @mcp.tool() and call reader.search(LOG_DIR, pattern, level, limit).


# TODO: Implement `count_logs_by_level`.
#
# The tool should return a dict of level -> count across all log files.
# Call reader.count_by_level(LOG_DIR).


# TODO: Implement `rotate_log_file`. This is a WRITE operation.
#
# The tool archives the named log file with a UTC timestamp suffix and
# creates a new empty file in its place. Be explicit in the description
# that this tool MODIFIES the filesystem. Call reader.rotate_log(LOG_DIR,
# filename).


if __name__ == "__main__":
    mcp.run()
