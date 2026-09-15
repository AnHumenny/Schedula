from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.schedule.models import ScheduleItem
    from app.modules.users.models import User
    from app.modules.groups.models import Group


class Profile(Base):
    """Database model for a profile."""

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    schedule_items: Mapped[list["ScheduleItem"]] = relationship(
        secondary="schedule_audience",
        back_populates="profiles",
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="profile",
    )

    groups: Mapped[list["Group"]] = relationship(back_populates="profile")
