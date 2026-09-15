from app.core.security import create_access_token, verify_password
from app.modules.users.models import User
from app.modules.users.repository import UserRepository


class AuthService:
    """Service for user authentication and token generation."""

    def __init__(self, user_repo: UserRepository):
        """Initialize AuthService with a user repository."""
        self.user_repo = user_repo


    async def authenticate(self, identifier: str, password: str) -> User | None:
        """Authenticate user by username/email and password, return user or None."""
        user = await self.user_repo.get_by_username(identifier)

        if not user:
            user = await self.user_repo.get_by_email(identifier)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user


    @staticmethod
    def make_token(user: User) -> str:
        """Create a JWT access token for the given user."""
        return create_access_token(
            {"sub": str(user.id), "role": user.role.value}
        )