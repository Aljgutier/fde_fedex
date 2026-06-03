# MCP Tool Security and Risk

This lab picks up where the MCP Tool Design lab left off. The `log_tools` MCP server is already complete — your job is not to add more tools but to decide which existing tools are *safe to run autonomously* and which need guardrails.

## Layout

```
.
├── log_tools/              # Complete server (from MCP Tool Design lab)
│   ├── reader.py
│   └── server.py
├── net_tools/              # Second server for Challenge 1 (network access)
│   └── server.py           # stub — implement the allowlist
├── hooks/
│   └── pretooluse.py       # stub hook — implement the denial logic
├── sample_logs/
│   └── app.log
├── secrets/                # Fake sensitive content for Challenge 2
│   ├── api_keys.txt
│   ├── db_password.env
│   └── customer_data.csv
├── TOOL_CLASSIFICATION.md  # classify each tool — fill in during Core Step 1
├── HOOK_TEMPLATE.md        # reference for the preToolUse hook contract
├── MCP_PERMISSIONS.md      # VS Code settings for per-tool confirmation
└── requirements.txt
```

## Setup

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

All `log_tools` tests should pass before you start. They verify the reader logic carried over from the previous lab.

## Important

The `secrets/` directory contains **fake, illustrative content**. None of the values are real credentials or customer data. They exist only to demonstrate content exclusion behavior in Challenge 2. Do not replace them with real secrets while working through this lab.
