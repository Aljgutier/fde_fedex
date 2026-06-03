# Feature Brief: Password Hashing Utility

## Summary

Implement a replacement for `src/utils.hash_password` and `src/utils.verify_password` that uses a modern key-derivation function with a per-password salt and constant-time verification. This is the Phase 4 cloud-agent task.

## Deliverables

1. A new module `src/password.py` with two public functions:
   - `hash_password(password: str) -> str`
   - `verify_password(password: str, stored: str) -> bool`
2. A test module `tests/test_password.py` covering every acceptance criterion below.
3. No edits to `src/utils.py`. The replacement is additive; migrating existing callers is a separate task not in this brief.

## Acceptance Criteria

### Hashing

- [ ] `hash_password` uses `hashlib.scrypt` (Python stdlib; no new dependencies). Parameters: `n=2**14`, `r=8`, `p=1`, `dklen=32`.
- [ ] Each call generates a fresh 16-byte random salt via `secrets.token_bytes(16)`.
- [ ] The returned string uses this format: `scrypt$<n>$<r>$<p>$<salt_b64>$<hash_b64>` where salt and hash are URL-safe base64 without padding.
- [ ] Two calls to `hash_password` with the same password return different strings (because the salt is different).

### Verification

- [ ] `verify_password` parses the stored string, recomputes the hash using the parsed parameters and salt, and compares in constant time using `hmac.compare_digest`.
- [ ] Returns `True` for a correct password; `False` for any incorrect password.
- [ ] Returns `False` (not raises) for a stored string that is malformed or uses an unknown algorithm prefix.

### Tests

- [ ] Round-trip: a hash produced by `hash_password` verifies successfully with `verify_password`.
- [ ] Hashes of the same password differ because of the fresh salt.
- [ ] `verify_password` returns `False` for a wrong password.
- [ ] `verify_password` returns `False` for a malformed stored string.
- [ ] `verify_password` uses `hmac.compare_digest` (test that importing the module does not shadow or replace it; an integration-style check is sufficient).

## Out of Scope

- Do not modify `src/utils.py`. The existing `hash_password` there stays as-is for Phase 4.
- Do not migrate `UserStore` or any other caller to the new utility.
- Do not introduce `bcrypt`, `argon2-cffi`, or any other dependency. `scrypt` is in the standard library for a reason.
- Do not add CLI wrappers, benchmarks, or documentation pages beyond the module docstring.

## Definition of Done

- `pytest` passes with no warnings.
- `python -c "from src.password import hash_password, verify_password; h = hash_password('hunter2'); assert verify_password('hunter2', h)"` exits 0.
- The diff touches only `src/password.py` and `tests/test_password.py`.
