import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal


SQL_FILE = (
    BASE_DIR
    / "app"
    / "modules"
    / "schedule"
    / "queries"
    / "delete_schedule_by_direction.sql"
)


async def delete_schedule(session: AsyncSession) -> None:
    sql = SQL_FILE.read_text(encoding="utf-8")

    commands = [
        command.strip()
        for command in sql.split(";")
        if command.strip()
    ]

    for command in commands:
        await session.execute(text(command))


async def test_delete() -> None:
    async with AsyncSessionLocal() as session:
        try:
            await delete_schedule(session)
            await session.commit()
            print("[delete schedule for direction] Successful!")
        except Exception:
            print("ERROR!")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(test_delete())
