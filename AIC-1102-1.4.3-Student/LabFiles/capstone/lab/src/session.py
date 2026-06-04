from datetime import datetime, timezone

from src.utils import generate_token


class SessionStore:
    def __init__(self):
        # FIXME: sessions live in memory only; restarts invalidate everyone
        self._sessions: dict[str, dict] = {}

    def create(self, email: str) -> str:
        token = generate_token()
        # TODO: add expires_at; sessions currently live forever
        self._sessions[token] = {
            "email": email,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        return token

    def get(self, token: str) -> dict | None:
        return self._sessions.get(token)

    def destroy(self, token: str) -> bool:
        return self._sessions.pop(token, None) is not None
