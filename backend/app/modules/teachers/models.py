from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.disciplines.models import Discipline
    from app.modules.schedule.models import ScheduleItem


class Teacher(Base):
    """Database model for a teacher."""

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
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

    disciplines: Mapped[list["Discipline"]] = relationship(
        secondary="teacher_discipline",
        back_populates="teachers",
        lazy="selectin",
    )

    schedule_items: Mapped[list["ScheduleItem"]] = relationship(
        back_populates="teacher",
        cascade="all, delete-orphan",
    )
