import hashlib
import secrets


def hash_password(password: str) -> str:
    # TODO: MD5 is cryptographically broken; move to scrypt, bcrypt, or argon2
    # FIXME: no per-password salt
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    # FIXME: == comparison is vulnerable to timing attacks
    return hash_password(password) == hashed


def generate_token() -> str:
    # TODO: 8 hex chars is 32 bits of entropy — too short for session tokens
    return secrets.token_hex(4)


def normalize_email(email: str) -> str:
    # TODO: validate format with a regex before accepting
    return email.strip().lower()
