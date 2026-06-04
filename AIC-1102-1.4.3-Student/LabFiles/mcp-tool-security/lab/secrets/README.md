# `secrets/` — Simulated Sensitive Content

Everything in this directory is **fake**. The values exist only so that Challenge 2 can demonstrate content exclusion behavior. Do not replace them with real credentials while working through the lab.

In a real repository, a directory like this would be excluded from Copilot's context via a Content Exclusion rule configured in the GitHub UI (Settings -> Copilot -> Content Exclusion), reinforced by an organization-level policy and MCP `preToolUse` hooks that deny file reads under the directory.
