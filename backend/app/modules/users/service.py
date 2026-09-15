from typing import TYPE_CHECKING, List

from sqlalchemy import select, func

from app.core.security import hash_password
from app.modules.users.enums import UserRole
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate

if TYPE_CHECKING:
    from app.modules.groups.repository import GroupRepository
    from app.modules.profiles.repository import ProfileRepository


class UserService:
    """Service for managing user accounts."""

    def __init__(
        self,
        repo: UserRepository,
        group_repo: "GroupRepository",
        profile_repo: "ProfileRepository",
    ):
        """Initialize the user service."""
        self.repo = repo
        self.group_repo = group_repo
        self.profile_repo = profile_repo


    async def get_user(self, user_id: int) -> UserRead:
        """Retrieve a user by their ID."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserRead.model_validate(user)


    async def list_users(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[UserRead]:
        """Retrieve a list of users with pagination."""
        users = await self.repo.list(limit, offset)
        return [UserRead.model_validate(u) for u in users]


    async def create_user(self, data: UserCreate) -> UserRead:
        """Create a new user account."""
        # 1. Уникальность
        if await self.repo.get_by_email(data.email):
            raise ValueError(f"Email {data.email} already registered")
        if await self.repo.get_by_username(data.username):
            raise ValueError(f"Username {data.username} already taken")

        if data.group_id is not None:
            group = await self.group_repo.get_by_id(data.group_id)
            if not group:
                raise ValueError(f"Group {data.group_id} not found")

        if data.profile_id is not None:
            profile = await self.profile_repo.get_by_id(data.profile_id)
            if not profile:
                raise ValueError(f"Profile {data.profile_id} not found")

        user = User(
            email=data.email,
            username=data.username,
            role=data.role,
            password_hash=hash_password(data.password),
            group_id=data.group_id,
            profile_id=data.profile_id,
        )
        user = await self.repo.create(user)
        return UserRead.model_validate(user)


    async def update_user(
        self,
        user_id: int,
        data: UserUpdate,
    ) -> UserRead:
        """Update an existing user account."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        payload = data.model_dump(exclude_unset=True)

        if "email" in payload and payload["email"] is not None:
            if payload["email"] != user.email:
                if await self.repo.get_by_email(payload["email"]):
                    raise ValueError(
                        f"Email {payload['email']} already registered"
                    )

        if "username" in payload and payload["username"] is not None:
            if payload["username"] != user.username:
                if await self.repo.get_by_username(payload["username"]):
                    raise ValueError(
                        f"Username {payload['username']} already taken"
                    )

        if "group_id" in payload and payload["group_id"] is not None:
            group = await self.group_repo.get_by_id(payload["group_id"])
            if not group:
                raise ValueError(f"Group {payload['group_id']} not found")

        if "profile_id" in payload and payload["profile_id"] is not None:
            profile = await self.profile_repo.get_by_id(payload["profile_id"])
            if not profile:
                raise ValueError(f"Profile {payload['profile_id']} not found")

        for field, value in payload.items():
            setattr(user, field, value)

        user = await self.repo.update(user)
        return UserRead.model_validate(user)


    async def delete_user(self, user_id: int) -> None:
        """Delete a user account by its ID."""

        if user_id == 1:
            raise PermissionError("Нельзя удалить главного администратора")

        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if user.role == UserRole.ADMIN:
            count_q = (
                select(func.count())
                .select_from(User)
                .where(User.role == UserRole.ADMIN)
            )
            admins_count = (
                await self.repo.session.execute(count_q)
            ).scalar_one()

            if admins_count <= 1:
                raise PermissionError(
                    "Нельзя удалить единственного администратора"
                )

        await self.repo.delete(user)
