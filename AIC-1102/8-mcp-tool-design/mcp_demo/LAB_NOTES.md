# LAB Notes 
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



