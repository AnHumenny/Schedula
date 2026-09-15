import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import app.core.models_registry  # noqa:

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.modules.users.enums import UserRole
from app.modules.users.models import User

ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD_PLAIN = "admin123"


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    q = select(User).where(User.email == email)
    return (await session.execute(q)).scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    q = select(User).where(User.username == username)
    return (await session.execute(q)).scalar_one_or_none()


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        existing_email = await get_user_by_email(session, ADMIN_EMAIL)
        if existing_email:
            print(f"[admin] SKIP {ADMIN_EMAIL} — email уже занят "
                  f"(id={existing_email.id})")
            return

        existing_username = await get_user_by_username(session, ADMIN_USERNAME)
        if existing_username:
            print(f"[admin] SKIP {ADMIN_USERNAME} — username уже занят "
                  f"(id={existing_username.id})")
            return

        admin = User(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            password_hash=hash_password(ADMIN_PASSWORD_PLAIN),
            role=UserRole.ADMIN,
            is_active=True,
            group_id=None,
        )
        session.add(admin)
        await session.flush()
        await session.commit()

        print(f"[admin] {admin.username} (id={admin.id}) создан")
        print(f"Пароль: {ADMIN_PASSWORD_PLAIN}")


if __name__ == "__main__":
    asyncio.run(seed())
