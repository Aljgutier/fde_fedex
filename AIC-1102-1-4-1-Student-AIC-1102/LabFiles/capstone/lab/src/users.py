from src.utils import hash_password, normalize_email


class UserStore:
    def __init__(self):
        self._users: dict[str, dict] = {}

    def create(self, email: str, password: str) -> dict:
        email = normalize_email(email)
        # FIXME: silently overwrites existing users with the same email
        # TODO: record a created_at timestamp
        self._users[email] = {
            "email": email,
            "password_hash": hash_password(password),
        }
        return self._users[email]

    def get(self, email: str) -> dict | None:
        return self._users.get(normalize_email(email))

    def update_password(self, email: str, new_password: str) -> bool:
        user = self.get(email)
        if user is None:
            return False
        user["password_hash"] = hash_password(new_password)
        return True

    def delete(self, email: str) -> bool:
        return self._users.pop(normalize_email(email), None) is not None
