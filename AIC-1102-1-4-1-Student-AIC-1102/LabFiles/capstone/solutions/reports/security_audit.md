# Security Audit — Reference Output

Example of what Phase 1's Copilot-generated audit should look like when the `grep -nR "TODO\|FIXME" src/` evidence is piped into `copilot -p`.

## Findings

### CRITICAL

#### `src/utils.py:5` — MD5 used for password hashing

- Evidence: `# TODO: MD5 is cryptographically broken; move to scrypt, bcrypt, or argon2`
- Reason: MD5 is not collision-resistant and has no work factor. Passwords stored in the database can be cracked at millions of attempts per second on commodity hardware.
- Recommendation: replace with `hashlib.scrypt` (Python stdlib) with a per-password random salt. See `FEATURE_BRIEF.md` for the Phase 4 replacement.
- Priority: address before any production deployment.

#### `src/utils.py:6` — No per-password salt

- Evidence: `# FIXME: no per-password salt`
- Reason: identical passwords produce identical hashes, enabling rainbow-table lookups. Even moving off MD5 without adding a salt leaves this class of attack viable.
- Recommendation: fixed together with the algorithm replacement above.
- Priority: same as the algorithm replacement — they must ship together.

#### `src/utils.py:11` — Timing-attack-vulnerable password comparison

- Evidence: `# FIXME: == comparison is vulnerable to timing attacks`
- Reason: `str.__eq__` short-circuits on the first differing byte. An attacker with request-latency observability can extract a hash byte by byte.
- Recommendation: use `hmac.compare_digest` for all comparisons of hash-equal-to-stored-hash.
- Priority: address in the Phase 4 replacement utility.

### HIGH

#### `src/utils.py:16` — Session tokens are 32 bits

- Evidence: `# TODO: 8 hex chars is 32 bits of entropy — too short for session tokens`
- Reason: 32-bit tokens collide after ~65k sessions (birthday bound) and are brute-forceable by an attacker with modest bandwidth.
- Recommendation: generate 32-character hex tokens (128 bits) via `secrets.token_hex(16)`.
- Priority: fix in the next sprint; no data-at-rest exposure but an active session-hijack surface.

#### `src/users.py:11` — Silent overwrite on duplicate email

- Evidence: `# FIXME: silently overwrites existing users with the same email`
- Reason: registering the same email twice replaces the prior user — effectively an account-takeover primitive if combined with a self-service "register" endpoint.
- Recommendation: raise `ValueError` on duplicate; require a separate `update_password` or admin path for legitimate overwrites.
- Priority: fix before any public registration endpoint is added.

#### `src/auth.py:16` — Email-existence oracle via login response

- Evidence: `# FIXME: returning None immediately here leaks whether the email exists`
- Reason: a different response time (or path) for "unknown email" vs. "bad password" lets an attacker enumerate valid emails.
- Recommendation: run verification against a dummy hash when the user is missing, so the timing and response shape are the same in both branches.
- Priority: address alongside rate limiting (`src/auth.py:10`) — both are pre-authentication enumeration defenses.

### MEDIUM

#### `src/auth.py:10` — No rate limiting on registration

- Evidence: `# FIXME: no rate limiting`
- Reason: permits abuse vectors (bulk account creation, email-bombing the verification flow).
- Recommendation: add rate limiting at the API boundary, not inside the function. Out of scope for a utility layer.
- Priority: plan for; not a utility-layer fix.

#### `src/session.py:7` — Sessions in-memory only

- Evidence: `# FIXME: sessions live in memory only; restarts invalidate everyone`
- Reason: availability concern more than security; noted for completeness since the session store needs redesign anyway.
- Recommendation: move to a signed-cookie or backing-store model in a follow-up.
- Priority: non-urgent.

### LOW

#### Ordinary code-quality TODOs

- `src/utils.py:20` — email format validation (UX, not security)
- `src/users.py:12` — `created_at` timestamp (observability, not security)
- `src/session.py:15` — session expiry (security-adjacent, noted together with in-memory session store)

These are worth tracking but do not alter the priority stack.

## Prioritization Summary

The three CRITICAL findings (lines 5, 6, 11 of `src/utils.py`) describe one connected problem: the password hashing subsystem is broken from algorithm through salt through comparison. Address all three in a single change. The Phase 4 feature brief specifies exactly that change.

The HIGH findings are each independent and can ship separately.

## What Copilot Added Beyond `grep`

- Rank-ordering by impact rather than file order
- Grouping of related findings (the three CRITICAL password-hashing issues)
- Explicit attack reasoning for each finding (not present in the source comments)
- Cross-reference to `FEATURE_BRIEF.md` for the CRITICAL cluster
- Distinguishing security-adjacent code-quality TODOs from the rest so the audit does not drown in noise
