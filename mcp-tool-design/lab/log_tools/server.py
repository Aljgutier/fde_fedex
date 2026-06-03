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


@mcp.tool()
def search_logs(pattern, level=None, limit=100) -> list[dict]:
    """Search log messages for entries matching a regex pattern.
    
    Args:
        pattern (str): The regex pattern to search for in log messages.
        level (str, optional): The log level to filter by (DEBUG, INFO, WARNING, ERROR).
        limit (int, optional): The maximum number of results to return (default 100).


    Returns:
        List[dict] with fields:
        {
            "file": str,
            "line_number": int,
            "timestamp": str,
            "level": str,
            "message": str
        }

    """

    return search(LOG_DIR, pattern, level, limit)

@mcp.tool()
def count_logs_by_level() -> dict:
    """Count the number of log entries at each level across all log files.

    Use this tool when the user wants an overview of the distribution of log
    levels in the logs.

    Returns:
        A dict mapping log levels (DEBUG, INFO, WARNING, ERROR) to their respective counts.
    """
    return count_by_level(LOG_DIR)

#@mcp.tool()
#def rotate_log_file(filename) -> None:
#    """Rotate a log file by archiving it with a timestamp and creating a new empty file.
#
#    This tool modifies the filesystem. It should be used when the user wants to
#    archive an existing log file and start fresh with a new empty log file.#
#    Args:
#        filename (str): The name of the log file to rotate (relative to the log directory).
#    """
#    rotate_log(LOG_DIR, filename)
#
#
#if __name__ == "__main__":
#    mcp.run()
