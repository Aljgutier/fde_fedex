import pytest

from src.users import UserStore


def test_create_and_get_user():
    store = UserStore()
    store.create("a@example.com", "password123")
    assert store.get("a@example.com") is not None


def test_emails_normalized_on_read_and_write():
    store = UserStore()
    store.create("A@Example.com", "password")
    assert store.get("a@example.com") is not None


def test_update_password_changes_hash():
    store = UserStore()
    store.create("a@example.com", "old")
    old_hash = store.get("a@example.com")["password_hash"]
    assert store.update_password("a@example.com", "new") is True
    assert store.get("a@example.com")["password_hash"] != old_hash


def test_update_missing_user_returns_false():
    store = UserStore()
    assert store.update_password("missing@example.com", "x") is False


def test_delete_user():
    store = UserStore()
    store.create("a@example.com", "p")
    assert store.delete("a@example.com") is True
    assert store.get("a@example.com") is None


def test_duplicate_email_rejected():
    """Registering the same email twice must not silently overwrite."""
    store = UserStore()
    store.create("a@example.com", "p1")
    with pytest.raises(Exception):
        store.create("a@example.com", "p2")
