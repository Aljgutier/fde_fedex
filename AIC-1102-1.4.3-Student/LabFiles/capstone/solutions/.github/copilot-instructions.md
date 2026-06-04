# Repository Conventions

These conventions apply to every file in this repository unless a path-specific instructions file overrides them.

## Language and stack

- Python 3.13+. Use the standard library first; new third-party dependencies must be surfaced explicitly in the Chat response before `requirements.txt` is edited.
- Tests use `pytest`. Do not introduce `unittest.TestCase` subclasses.

## Naming

- `snake_case` for functions, variables, and modules. `UPPER_SNAKE_CASE` for module-level constants. `PascalCase` for classes.
- Test functions: `test_<action>_<expected_outcome>`.

## Security posture

- Any new password-handling or credential-handling code must use a constant-time comparison (`hmac.compare_digest`) for matches.
- Any new random-generation code used in a security context must use `secrets`, never `random`.
- Any new session token must be at least 16 random bytes (32 hex chars).
- Never introduce a timing oracle on authentication paths.

## Response shape

- Functions that search for an optional record return `None` on absence, do not raise.
- Functions that create a resource raise on uniqueness violations rather than silently overwriting.

## Scope discipline

- Do not edit files outside the directory implied by the task without explicitly stating that you are doing so and why.
- Do not introduce unrelated refactors, renames, or cleanups into a task that did not request them.
