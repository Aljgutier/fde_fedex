"""Password hashing utility using scrypt.

This module is the Phase 4 feature target. It replaces the broken
``hash_password``/``verify_password`` pair in ``src/utils.py`` for any
future caller. The legacy pair remains in place so this change does not
break existing tests; callers migrate in a follow-up task.
"""

import base64
import hashlib
import hmac
import secrets

_ALGORITHM = "scrypt"
_N = 2**14
_R = 8
_P = 1
_DKLEN = 32
_SALT_BYTES = 16


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded)


def _derive(password: str, salt: bytes, n: int, r: int, p: int, dklen: int) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=n,
        r=r,
        p=p,
        dklen=dklen,
    )


def hash_password(password: str) -> str:
    """Return a salted scrypt hash of ``password`` in the module's string format."""
    salt = secrets.token_bytes(_SALT_BYTES)
    derived = _derive(password, salt, _N, _R, _P, _DKLEN)
    return f"{_ALGORITHM}${_N}${_R}${_P}${_b64encode(salt)}${_b64encode(derived)}"


def verify_password(password: str, stored: str) -> bool:
    """Return True iff ``password`` verifies against ``stored``. False on malformed input."""
    try:
        parts = stored.split("$")
        if len(parts) != 6:
            return False
        algorithm, n_str, r_str, p_str, salt_b64, hash_b64 = parts
        if algorithm != _ALGORITHM:
            return False
        n, r, p = int(n_str), int(r_str), int(p_str)
        salt = _b64decode(salt_b64)
        expected = _b64decode(hash_b64)
    except (ValueError, base64.binascii.Error):
        return False

    computed = _derive(password, salt, n, r, p, len(expected))
    return hmac.compare_digest(computed, expected)
