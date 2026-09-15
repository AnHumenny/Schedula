from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.teachers.models import Teacher
    from app.modules.schedule.models import ScheduleItem


# ---------------------------------------------------------------------------
# Intermediate table for Teacher N:N Discipline.
# Declared here to break the teachers ↔ disciplines cycle:
# both sides reference it via secondary="teacher_discipline".
# No cross-module imports.
# ---------------------------------------------------------------------------
teacher_discipline = Table(
    "teacher_discipline",
    Base.metadata,
    Column(
        "teacher_id",
        ForeignKey("teachers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "discipline_id",
        ForeignKey("disciplines.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Discipline(Base):
    """Academic subject/discipline taught by teachers."""
    __tablename__ = "disciplines"

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

    teachers: Mapped[list["Teacher"]] = relationship(
        secondary="teacher_discipline",
        back_populates="disciplines",
        lazy="selectin",
    )

    schedule_items: Mapped[list["ScheduleItem"]] = relationship(
        back_populates="discipline",
    )
