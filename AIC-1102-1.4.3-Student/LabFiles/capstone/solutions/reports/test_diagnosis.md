## tests/test_users.py::test_duplicate_email_rejected

**Assertion or error:** `Failed: DID NOT RAISE <class 'Exception'>`

**Root cause hypothesis:** `UserStore.create` silently overwrites the existing entry when the normalized email is already present. The test expects the second call to raise. Matches the `# FIXME: silently overwrites existing users with the same email` comment on the same method.

**Proposed fix:** `src/users.py`

```diff
 def create(self, email: str, password: str) -> dict:
     email = normalize_email(email)
-    # FIXME: silently overwrites existing users with the same email
-    # TODO: record a created_at timestamp
+    if email in self._users:
+        raise ValueError(f"user already exists: {email}")
     self._users[email] = {
         "email": email,
         "password_hash": hash_password(password),
     }
     return self._users[email]
```

---

## tests/test_auth.py::test_session_token_is_sufficiently_long

**Assertion or error:** `AssertionError: assert len(token) >= 32`

**Root cause hypothesis:** `generate_token` produces 8 hex characters (4 random bytes). The test requires 32 hex characters (16 random bytes) to guarantee 128 bits of entropy for session tokens. Matches the `# TODO: 8 hex chars is 32 bits of entropy — too short for session tokens` comment.

**Proposed fix:** `src/utils.py`

```diff
 def generate_token() -> str:
-    # TODO: 8 hex chars is 32 bits of entropy — too short for session tokens
-    return secrets.token_hex(4)
+    return secrets.token_hex(16)
```

---

*Reference output only. Your actual Phase 2 diagnosis will vary in wording; the section structure should match.*
