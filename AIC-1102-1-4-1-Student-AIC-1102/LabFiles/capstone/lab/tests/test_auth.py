import pytest

from src.auth import login, logout, register, sessions, users


def setup_function():
    users._users.clear()
    sessions._sessions.clear()


def test_register_creates_user():
    u = register("a@example.com", "p")
    assert u["email"] == "a@example.com"


def test_login_returns_session_token():
    register("a@example.com", "p")
    token = login("a@example.com", "p")
    assert token is not None


def test_login_rejects_wrong_password():
    register("a@example.com", "p")
    assert login("a@example.com", "wrong") is None


def test_logout_destroys_session():
    register("a@example.com", "p")
    token = login("a@example.com", "p")
    assert logout(token) is True
    assert sessions.get(token) is None


def test_session_token_is_sufficiently_long():
    """Session tokens must be at least 32 hex characters (128 bits of entropy)."""
    register("a@example.com", "p")
    token = login("a@example.com", "p")
    assert len(token) >= 32
