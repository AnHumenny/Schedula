import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Table, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.profiles.models import Profile
    from app.modules.teachers.models import Teacher
    from app.modules.disciplines.models import Discipline
    from app.modules.locations.rooms.models import Room
    from app.modules.groups.models import Group


class LessonType(str, enum.Enum):
    """Enumeration of available lesson types."""

    LECTURE = "LECTURE"
    PRACTICE = "PRACTICE"
    LAB = "LAB"
    SEMINAR = "SEMINAR"
    EXAM = "EXAM"
    CONSULTATION = "CONSULTATION"


class LessonStatus(str, enum.Enum):
    """Enumeration of possible lesson statuses."""

    PLANNED = "PLANNED"
    CANCELLED = "CANCELLED"
    RESCHEDULED = "RESCHEDULED"


schedule_audience = Table(
    "schedule_audience",
    Base.metadata,
    Column(
        "schedule_item_id",
        ForeignKey("schedule_items.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "profile_id",
        ForeignKey("profiles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


schedule_groups = Table(
    "schedule_groups",
    Base.metadata,
    Column(
        "schedule_item_id",
        ForeignKey("schedule_items.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "group_id",
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ScheduleItem(Base):
    """Database model representing a scheduled lesson item."""

    __tablename__ = "schedule_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    profiles: Mapped[list["Profile"]] = relationship(
        secondary="schedule_audience",
        back_populates="schedule_items",
        lazy="selectin",
    )

    groups: Mapped[list["Group"]] = relationship(
        secondary="schedule_groups",
        back_populates="schedule_items",
        lazy="selectin",
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    discipline_id: Mapped[int] = mapped_column(
        ForeignKey("disciplines.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    start_datetime: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    lesson_type: Mapped[LessonType] = mapped_column(
        Enum(LessonType, name="lessontype"),
        default=LessonType.LECTURE,
        nullable=False,
    )
    status: Mapped[LessonStatus] = mapped_column(
        Enum(LessonStatus, name="lessonstatus"),
        default=LessonStatus.PLANNED,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    teacher: Mapped["Teacher"] = relationship(back_populates="schedule_items")
    discipline: Mapped["Discipline"] = relationship(back_populates="schedule_items")
    room: Mapped["Room"] = relationship(back_populates="schedule_items")
