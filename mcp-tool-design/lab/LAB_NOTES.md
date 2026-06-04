# LAB_NOTES_SELECTION 

# pytest
pytest ... needs to run as
pytest needs to be run with
```sh
pytest -m pytest
```

# TOOL SELECTION RESULTS

* overall seemed to work well
* had to make improvements to the return structure of the search tool



##GitHub MCP BENCHARK##
Server: Example Exposed Tools

The GitHub MCP server exposes tools for GitHub workflows (issues, pull requests, repositories, search, and more).

| Name | Description |
|---|---|
| create_pull_request | Open new pull request |
| list_pull_requests | List pull requests |
| list_issue_types | List available issue types |

## 7.3.43Add two new tools 
***log-tools MCP server: exposed tools***
Ask agent how many tools it finds ... make sure to **CTRL-SHFT-P Developer: Reload Window**

Prompt (Agent)
* What tools does the log-tools MCP server expose? List their
names and one-line descriptions.

Agent Response
- list_logs: List the log files available in the configured log directory.
- search_logs: Search log messages for entries matching a regex pattern.
- count_logs_by_level: Count the number of log entries at each level across all log files.

## 7.3.4 Selection Accuracy

Use the search_logs tool and return the full structured results without summarizing.


prompt

    - Use the search_logs tool and return the full structured results without summarizing.

I’ll execute the actual search_logs function from the MCP server code with the redis + ERROR query and return the raw structured payload exactly as produced


## MCP Model Test Python Code Execution Result

**Python Interpreter:** `file:///c%3A/LabFiles/fde_repo/mcp-tool-design/lab/.venv/Scripts/python.exe`

**Exit Code:** 0

**Code Lines:** 5

**Working Directory:** `file:///c%3A/LabFiles/fde_repo/mcp-tool-design/lab`

***Executed Code:***

```python
import json
from log_tools.server import search_logs

results = search_logs(pattern="redis", level="ERROR", limit=100)
print(json.dumps(results, indent=2))
```

***Output (stdout and stderr interleaved)***:

```
[
  {
    "file": "app.log",
    "line_number": 5,
    "timestamp": "2026-01-15T10:01:03Z",
    "level": "ERROR",
    "message": "Failed to connect to redis: connection refused"
  },
  {
    "file": "app.log",
    "line_number": 6,
    "timestamp": "2026-01-15T10:01:04Z",
    "level": "ERROR",
    "message": "Retrying redis connection (attempt 1/5)"
  }
]
```

***About This Tool***

This tool executes Python code directly without shell quoting issues that would occur with `python -c`. It's ideal for running one-off Python snippets without creating temporary files. The output shows stdout and stderr interleaved in chronological order, giving you the exact sequence of output as it would appear when running the code in a terminal.


## 7.3.5 Add the Write Tool .... Rotate Log Files
* implement 

Prompt
* What tools does the log-tools MCP server expose? List their
names and one-line descriptions.

Agent Result  

    - list_logs: Lists log files available in the configured log directory.
    - search_logs: Searches log messages for entries matching a regex pattern, with optional level filtering and result limit.
    - count_logs_by_level: Counts log entries by level across all log files.
    - rotate_log_file: Rotates a log file by archiving it with a timestamp and creating a new empty file.


Results ...

Rotation completed successfully.

    - Rotated file: app.log
    - New archive created: app.log.20260604T155722Z.archive
    - Fresh active log remains: app.log


7.3.6 Raise Value Error ... tool break


prompt

    - Use the search_logs tool and return the full structured results without summarizing.

raise ValueError("search unavailable")


Results:

`
The tool call failed because the current server implementation is returning search unavailable; I’ll inspect the live server code and then call the underlying search logic to still provide the full structured results.

The tool call failed because the current server implementation is returning search unavailable; I’ll inspect the live server code and then call the underlying search logic to still provide the full structured results.
`


# Appendex - LAB Notes from Class

https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem

See the Anthropic website ... this tool simply access the file system tool 

Go to Anthropic and get VSCODE mcp.json file 

Gets node package from npm and running it s

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${workspaceFolder}"
      ]
    }
  }
}
```

Python Server Example

```json
{
  "servers": {
    "log-tools": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "log_tools.server"],
      "cwd": "C:/LabFiles/mcp-tool-design/lab",
      "env": {
        "LOG_DIR": "C:/LabFiles/mcp-tool-design/lab/sample_logs"
      }
    }
  }
}

```

"Here's a server called log-tools. To start it, run python -m  log_tools.server in this folder, and tell it the logs live in sample_logs."

* note that it starts the venv ... could also put the .venv in Path  spec
* cwd - current working directory
* sdio is like a shell
* env is like the variables for 

```json
{
  "servers": {
    "log-tools": {
      "type": "stdio",
      "command": "C:/LabFiles/AIC-1102/LabFiles/mcp-tool-design/lab/.venv/Scripts/python.exe",
      "args": ["-m", "log_tools.server"],
      "cwd": "C:/LabFiles/AIC-1102/LabFiles/mcp-tool-design/lab",
      "env": {
        "LOG_DIR": "C:/LabFiles/AIC-1102/LabFiles/mcp-tool-design/lab/sample_logs"
      }
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

* CTRL-SHIFT-P MCP  list servers to  can also start and stop servers 
* The AI will also often bypass the MCPs without saying so. Watch the output for clues or ask explicitly periodically.
* rpslace C:/LabFiles/AIC-1102/LabFiles/mcip-tool-design/lab with  ${workspaceFolder}

