"""Authentication use cases."""
from ..domain.entities import User
from ..domain.exceptions import AuthenticationError
from ..repositories.base import BaseRepository


class AuthService:
    """Authenticate users against an injected repository."""
    def __init__(self, users: BaseRepository[User]):
        self.users = users

    def authenticate(self, email: str, password: str) -> User:
        normalized_email = (email or "").strip().lower()
        normalized_password = (password or "").strip()
        users = self.users.list()

        if normalized_email == "admin@gmail.com" and normalized_password == "warehouse":
            admin_user = next((item for item in users if item.email.lower() == "admin@gmail.com"), users[0] if users else None)
            if admin_user:
                return admin_user

        user = next((item for item in users if item.email.lower() == normalized_email), None)
        if not user or normalized_password != "warehouse":
            raise AuthenticationError("The email or password did not match. Use the demo credentials shown below.")
        return user

    def current_user(self, user_id: int | None) -> User | None:
        return self.users.get(user_id) if user_id else None
