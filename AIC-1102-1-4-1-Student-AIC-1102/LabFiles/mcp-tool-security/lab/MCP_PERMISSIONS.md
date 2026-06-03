# MCP Tool Permissions in VS Code

VS Code Copilot lets you configure which MCP tools run without confirmation and which require explicit approval before each call. As of April 2026, per-tool confirmation is a **runtime UI toggle** — not a JSON config key. Older community examples on the web still show a `toolPermissions` map; that shape is not honored by current VS Code builds and will be silently ignored. Use the UI toggle documented below.

## Server Registration (JSON)

MCP servers are declared in `.vscode/mcp.json` (workspace-scoped) or the user-level `mcp.json`. The file has a top-level `servers` key:

```json
{
  "servers": {
    "log-tools": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "log_tools.server"],
      "cwd": "<absolute-path>",
      "env": { "LOG_DIR": "<absolute-path>/sample_logs" }
    }
  }
}
```

Per-tool confirmation settings are **not** expressed here. They live in the MCP tools picker (see below).

## Per-Tool Confirmation (UI Toggle)

1. Open Copilot Chat and expand the tools picker (the wrench icon above the chat input, or **Chat: Configure Tools** from the command palette).
2. Locate your `log-tools` server and expand it to see each tool by name.
3. For every tool you classified as Safe, click the tool row and enable **Always allow**. The toggle persists per workspace and is reflected in the icon next to the tool name.
4. For every tool you classified as High-Risk, leave **Always allow** off. That tool will prompt for confirmation on every call.

The toggle state is stored by VS Code in its workspace storage — you do not need to commit a config file for it to persist for *your* workspace, but teammates will each set their own toggles unless you share a recommended configuration separately.

## Verifying the Configuration

1. Issue a prompt that triggers a Safe tool (for example, `search_logs`). The tool should run without a confirmation modal.
2. Issue a prompt that triggers a High-Risk tool (`rotate_log_file`). The tool should show a confirmation modal with the tool name and arguments. Approving proceeds; declining aborts.
3. Inspect the Agent Logs. You should see the confirmation event recorded, not just the eventual call outcome.

## Copilot CLI Equivalent

Outside of VS Code, Copilot CLI exposes per-tool permission through command-line flags rather than a UI toggle:

- `--allow-tool <server>.<tool>` pre-approves a specific tool for the session (repeat the flag for multiple tools).
- `--allow-all-tools` pre-approves every tool for the session. Treat this as the CLI equivalent of "blanket always-allow" — reserve it for sandboxed runs (CI, scripted pipelines) where you control every tool the agent can see, and never use it interactively with a production-capable toolset.

A tool not covered by either flag prompts for confirmation when called. The CLI flag model is session-scoped, not persistent; there is no stored "always allow" analogue to the VS Code toggle.

## Scoping Permissions to the Project

The UI toggle is per-workspace by default — your approval for a destructive tool in one project does not leak to another. If you find yourself re-setting the same toggles in every project, that is a signal to re-classify the tool: Safe is a universal claim, not a per-project one.

## Permission vs. Hook

Permissions are user-level approvals. A confirmation modal is a binary choice by the human.

Hooks are machine-level gates. A hook can deny an *otherwise-approved* call based on arguments, flags, or derived properties the user would not catch in a modal (path traversal, unusual flags).

Use both:

- Permissions to mark that a tool is High-Risk (so the human is asked).
- Hooks to refuse specific patterns even when the human would approve.
