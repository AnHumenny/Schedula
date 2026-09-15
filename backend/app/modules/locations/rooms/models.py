from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.locations.buildings.models import Building
    from app.modules.schedule.models import ScheduleItem


class Room(Base):
    """Database model for a room."""

    __tablename__ = "rooms"

    __table_args__ = (
        UniqueConstraint("building_id", "number", name="uq_room_building_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    number: Mapped[str] = mapped_column(String(100), nullable=False)

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

    building: Mapped["Building"] = relationship(
        back_populates="rooms",
        lazy="raise",
    )

    schedule_items: Mapped[list["ScheduleItem"]] = relationship(
        back_populates="room",
        lazy="raise",
    )
