# MCP (Model Context Protocol)

MCP (Model Context Protocol) is a universal standard that acts as a secure, shared language. It allows AI models (like Claude or ChatGPT) to safely connect to external data sources (like Google Drive, a local codebase, or Slack), enabling the AI to retrieve information and take action.

## The Problem It Solves

Historically, if you wanted an AI to access your company's database or your personal email, engineers had to write custom code for every single app to make it work with the AI.

Without MCP: The AI only knows what it was originally trained on and cannot access your private data unless you painstakingly paste it into the chat box.

With MCP: External tools use a standard set of rules to communicate with the AI. It acts as a universal adapter, meaning developers only have to set it up once, and the AI can seamlessly interact with hundreds of your everyday tools.

## How It Works

Think of MCP like a translator layer between an AI chat app and outside tools.

In simple terms, there are three parts:

- Host: The app you chat in (for example, VS Code chat).
- Client: The MCP feature inside the host that decides when to call a tool and formats requests.
- Server: A small program that exposes tools and runs real work (read files, query APIs, update systems).

Basic flow:

1. You ask a question in the host.
2. The client decides a tool is needed.
3. The client sends a structured MCP request to the server.
4. The server runs the tool and returns structured results.
5. The client gives results back to the host so the AI can answer.

## How It Works for Lab Project

In this lab, the host is your Copilot chat experience in VS Code.

The client is the MCP integration built into the host. It sees the tool descriptions and decides when to call the log tools.

The server is `log-tools`, started with Python in stdio mode. It runs `log_tools.server` and registers read tools such as:

- `list_logs`
- `search_logs`
- `count_logs_by_level`

The server reads the log directory from the `LOG_DIR` environment variable set in the MCP configuration, which points to the lab's `sample_logs` folder.

Lab request flow:

1. You ask something like "find redis errors".
2. The MCP client routes to `search_logs` based on the tool description.
3. `log_tools.server` calls reader logic and searches files in `sample_logs`.
4. Matching entries are returned to the client.
5. The host shows a natural-language answer built from those results.

## Why It Matters

Real-Time Data: Instead of guessing or hallucinating, the AI can securely pull real-time data directly from your local computer or company servers.

Automation: It enables AI to take actual action, like pulling a file from your hard drive, drafting an email in your drafts folder, or updating a spreadsheet.
