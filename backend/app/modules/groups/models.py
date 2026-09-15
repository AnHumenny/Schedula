from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.directions.models import Direction
    from app.modules.schedule.models import ScheduleItem
    from app.modules.users.models import User
    from app.modules.profiles.models import Profile


class Group(Base):
    """Academic group belonging to a direction and optionally a profile."""
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    direction_id: Mapped[int] = mapped_column(
        ForeignKey("directions.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    direction: Mapped["Direction"] = relationship(back_populates="groups")
    users: Mapped[list["User"]] = relationship(back_populates="group")
    schedule_items: Mapped[list["ScheduleItem"]] = relationship(
        secondary="schedule_groups",
        back_populates="groups",
    )

    profile_id: Mapped[int | None] = mapped_column(
        ForeignKey("profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    profile: Mapped["Profile | None"] = relationship(back_populates="groups")