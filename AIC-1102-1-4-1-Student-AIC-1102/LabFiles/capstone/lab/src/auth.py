from src.session import SessionStore
from src.users import UserStore
from src.utils import verify_password

users = UserStore()
sessions = SessionStore()


def register(email: str, password: str) -> dict:
    # TODO: enforce password complexity (length, classes)
    # FIXME: no rate limiting on registration
    return users.create(email, password)


def login(email: str, password: str) -> str | None:
    user = users.get(email)
    if user is None:
        # FIXME: returning None immediately here leaks whether the email exists
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return sessions.create(email)


def logout(token: str) -> bool:
    return sessions.destroy(token)
