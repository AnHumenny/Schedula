from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.groups.models import Group
  #  from app.modules.schedule.models import ScheduleItem


class Direction(Base):
    """Academic direction (program) for a given year."""
    __tablename__ = "directions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    academic_year: Mapped[str] = mapped_column(String(20))  # "2026-2027"
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    groups: Mapped[list["Group"]] = relationship(back_populates="direction")

    # schedule_items: Mapped[list["ScheduleItem"]] = relationship(
    #     secondary="schedule_audience",а
    #     back_populates="directions",
    # )