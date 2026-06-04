# Agent Behavioral Guidance

Additional constraints for autonomous agent sessions (Agent Mode, the cloud agent, Copilot CLI). These apply on top of `.github/copilot-instructions.md` and every path-specific instructions file.

## Hard constraints

- **Never run any command on the deny list in `DENY_LIST.md`.** The Phase 4 `preToolUse` hook enforces this at the tool level, but agents are expected to avoid the category regardless.
- **Never commit anything to `main` directly.** All work lands on feature branches.
- **Never modify `DENY_LIST.md`, `AGENTS.md`, or any file under `.github/` during a feature implementation task.** Configuration changes are a separate task type.
- **Never install a new dependency without stating the dependency and reason before modifying `requirements.txt`.**

## Before acting on a security-sensitive task

- State which `TODO` or `FIXME` comments in the repository are relevant to the task.
- If the task touches password handling, session tokens, or user identity, cite the security rules from `.github/instructions/audit.instructions.md` that apply.
- Propose the implementation plan (files to create, interfaces, tests) before editing any file.

## Scope

- Stay inside the directory implied by the task unless the change genuinely requires a cross-directory update.
- If a change would touch files in more than two top-level directories, pause and confirm the full list with the requester before proceeding.
- Do not "clean up" unrelated code while working on a scoped task. Surface the observation as a follow-up recommendation instead.

## Reporting

- After any task that adds new functionality, print a summary listing: files added, files modified, tests added, and any security rules from `audit.instructions.md` that the implementation satisfies.
- After any task that modifies authentication or credential handling, include a line stating: "Credential scan clean" (or, if the scan was skipped, "Credential scan not performed; reason: ...").
