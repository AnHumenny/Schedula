from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class UserRepository:
    """Repository for managing user data persistence."""

    def __init__(self, session: AsyncSession):
        """Initialize the user repository."""
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        return await self.session.get(User, user_id)


    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        q = select(User).where(User.email == email)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        q = select(User).where(User.username == username)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(self, limit: int = 50, offset: int = 0) -> List[User]:
        """Retrieve a list of users with pagination."""
        q = select(User).order_by(User.id).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def list_by_group(
        self, group_id: int, limit: int = 50, offset: int = 0
    ) -> List[User]:
        """Retrieve a list of users belonging to a specific group."""
        q = (
            select(User)
            .where(User.group_id == group_id)
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def list_by_profile(
        self, profile_id: int, limit: int = 50, offset: int = 0
    ) -> List[User]:
        """Retrieve a list of users associated with a specific profile."""
        q = (
            select(User)
            .where(User.profile_id == profile_id)
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def create(self, user: User) -> User:
        """Create a new user record."""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def update(self, user: User) -> User:
        """Update an existing user record."""
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def delete(self, user: User) -> None:
        """Delete a user record."""
        await self.session.delete(user)
        await self.session.commit()


    async def group_exists(self, group_id: int) -> bool:
        """Check whether a group with the given ID exists."""
        from app.modules.groups.models import Group
        return await self.session.get(Group, group_id) is not None


    async def profile_exists(self, profile_id: int) -> bool:
        """Check whether a profile with the given ID exists."""
        from app.modules.profiles.models import Profile
        return await self.session.get(Profile, profile_id) is not None