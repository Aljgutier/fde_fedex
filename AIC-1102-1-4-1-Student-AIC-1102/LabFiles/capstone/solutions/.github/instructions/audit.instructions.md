---
applyTo: "src/**/*.py"
---

# Source-Directory Instructions

These rules apply to the Python source files under `src/`. They refine the repository-wide conventions in `copilot-instructions.md` for code that handles authentication, sessions, and passwords.

## Security rules specific to `src/`

- Never write a password comparison using `==`. Use `hmac.compare_digest`.
- Never generate a security-sensitive value with `random`. Use `secrets`.
- Never log, print, or persist a plaintext password. Never log a full session token — truncate to the first 4 characters if diagnostic logging is needed.
- Never expose a distinction between "email does not exist" and "password is wrong" in any authentication response. Both must produce the same response shape and, ideally, similar timing.

## Response shape rules specific to `src/`

- `get` / `lookup` methods return `None` when the record is absent.
- `create` methods raise `ValueError` on uniqueness violations.
- `delete` methods return `bool` — `True` when something was removed, `False` when the key was absent.

## Audit remediation process

When asked to address a `TODO` or `FIXME` comment in this directory:

1. First restate the security concern in the Chat response in your own words, so the user can confirm the understanding before any code changes.
2. Propose the fix as a diff before applying it.
3. If the fix requires a change to an interface (return type, raised exception), explicitly call out the caller impact. Do not silently break callers.

## What not to do

- Do not rewrite existing `hash_password` in `src/utils.py` as part of any task unless the task explicitly requests that rewrite. The replacement path is `src/password.py` per `FEATURE_BRIEF.md`.
- Do not add dependencies. Use the standard library for crypto (`hashlib`, `hmac`, `secrets`).
