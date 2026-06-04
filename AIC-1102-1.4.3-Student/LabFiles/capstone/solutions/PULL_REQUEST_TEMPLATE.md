# Pull Request

## Summary

<!-- Two or three sentences on what this PR changes and why.  -->

## Related Issue

<!-- Closes #... or Refs #... -->

## Changes

- `src/password.py` — new module exposing `hash_password` and `verify_password`
- `tests/test_password.py` — coverage for round-trip, salt freshness, malformed input, algorithm prefix

<!-- Replace the above bullets with the actual list for this PR. -->

## Risk Assessment

### Security surface

- **Password hashing algorithm.** This PR introduces `scrypt` (stdlib, `n=2**14`, `r=8`, `p=1`). Risk: parameters are tuned for current compute; revisit in 12 months. Mitigation: parameters encoded in the stored string, so future hashes can use stronger parameters without breaking verification of existing hashes.
- **Comparison safety.** `verify_password` uses `hmac.compare_digest`. Risk: future callers may use `==` out of habit. Mitigation: `audit.instructions.md` rule forbidding `==` comparison for security-sensitive values; code review must verify.
- **Salt generation.** 16-byte random salt via `secrets.token_bytes`. Risk: no salt reuse expected; `secrets` is the correct primitive.
- **Malformed input handling.** `verify_password` returns `False` for malformed stored strings rather than raising. Risk: a silent `False` could mask an exploited downgrade (an attacker replaces a real hash with garbage and logs in with any password if a caller inverts the return). Mitigation: callers must treat `False` as authoritative "do not authenticate" and not retry with a different comparison.
- **Log exposure.** Neither plaintext nor stored hash is logged by this module. Risk: callers may log the return of `hash_password` believing it to be a "safe hash." Mitigation: `audit.instructions.md` rule — never log credential-derived values.

### Dependency surface

- No new dependencies. `scrypt`, `secrets`, and `hmac` are Python stdlib.

### Compatibility

- **Additive change.** `src/utils.hash_password` is unchanged. Existing callers continue to use MD5; they must be migrated in a separate task.
- **No schema change.** No database migration required.

### Rollback

- Revert this commit. No side effects beyond the two new files.

## Testing Steps

### Automated

- `pytest tests/test_password.py` — full module coverage (8 tests)
- `pytest` — all existing tests still pass

### Manual smoke

```bash
python -c "
from src.password import hash_password, verify_password
h = hash_password('hunter2')
assert verify_password('hunter2', h)
assert not verify_password('wrong', h)
print('ok')
"
```

### Integration verification (in-memory)

1. Import `hash_password` and `verify_password` into a scratch script.
2. Hash a known password; capture the stored string.
3. Call `verify_password` with the correct password — expect `True`.
4. Call `verify_password` with a wrong password — expect `False`.
5. Call `verify_password` with a malformed stored string (`"oops"`) — expect `False`, no exception.
6. Confirm two separate `hash_password` calls with the same password return different strings.

## Pre-Merge Checklist

- [ ] Acceptance criteria from `FEATURE_BRIEF.md` are each traceable to a test.
- [ ] No files outside `src/password.py` and `tests/test_password.py` are touched.
- [ ] `pytest` is green in CI.
- [ ] Reviewer has confirmed no `==` is used for credential comparison.
- [ ] Reviewer has read the Risk Assessment section and confirmed its accuracy.
- [ ] All hook denials from the implementing session have been triaged.

## Notes for Reviewer

This PR is scoped narrowly to the new utility. Migration of existing callers (`UserStore.create`, `UserStore.update_password`, `auth.login`) is a separate task. The legacy MD5 `hash_password` in `src/utils.py` remains in place for that reason.
