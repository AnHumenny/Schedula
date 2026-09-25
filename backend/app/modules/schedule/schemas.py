from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from app.modules.schedule.models import LessonType, LessonStatus


class ScheduleItemBase(BaseModel):
    """Base schema for schedule item data containing shared fields."""

    group_ids: list[int] = Field(default_factory=list, description="List of group IDs attending the lesson")
    teacher_id: int = Field(..., description="ID of the teacher conducting the lesson")
    discipline_id: int = Field(..., description="ID of the discipline being taught")
    room_id: int = Field(..., description="ID of the room where the lesson takes place")
    start_datetime: datetime = Field(..., description="Start date and time of the lesson")
    end_datetime: datetime = Field(..., description="End date and time of the lesson")
    lesson_type: LessonType = Field(LessonType.LECTURE, description="Type of the lesson")
    status: LessonStatus = Field(LessonStatus.PLANNED, description="Current status of the lesson")
    description: str | None = Field(None, description="Additional description or notes")


class ScheduleItemCreate(ScheduleItemBase):
    """Schema for creating a new schedule item."""

    pass


class ScheduleItemUpdate(BaseModel):
    """Schema for updating an existing schedule item."""

    group_ids: list[int] | None = Field(None, description="List of group IDs attending the lesson")
    teacher_id: int | None = Field(None, description="ID of the teacher conducting the lesson")
    discipline_id: int | None = Field(None, description="ID of the discipline being taught")
    room_id: int | None = Field(None, description="ID of the room where the lesson takes place")
    start_datetime: datetime | None = Field(None, description="Start date and time of the lesson")
    end_datetime: datetime | None = Field(None, description="End date and time of the lesson")
    lesson_type: LessonType | None = Field(None, description="Type of the lesson")
    status: LessonStatus | None = Field(None, description="Current status of the lesson")
    description: str | None = Field(None, description="Additional description or notes")


class ScheduleItemRead(ScheduleItemBase):
    """Schema for reading complete schedule item details."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the schedule item")
    group_ids: list[int] = Field(default_factory=list, description="List of group IDs attending the lesson")
    created_at: datetime = Field(..., description="Timestamp when the schedule item was created")
    updated_at: datetime = Field(..., description="Timestamp when the schedule item was last updated")


class ScheduleCopyBase(BaseModel):
    """Base schema for copying schedule."""

    source_start: date = Field(..., description="Start date of the source period")
    source_end: date = Field(..., description="End date of the source period")
    weeks_to_copy: int = Field(..., description="Number of weeks to copy")


class ScheduleCopyByGroupRequest(ScheduleCopyBase):
    """Schema for copying schedule by group."""
    group_id: int = Field(..., description="Group ID")


class ScheduleCopyByDirectionRequest(ScheduleCopyBase):
    """Schema for copying schedule by direction."""
    direction_id: int = Field(..., description="Direction ID")


class ScheduleDeleteByGroupRequest(BaseModel):
    """Schema for deleting schedule by group."""

    start_date: date = Field(..., description="Start date of the source period")
    weeks_to_delete: int = Field(..., description="Number of weeks to delete")
    group_id: int = Field(..., description="Group ID")


class ScheduleDeleteByDirectionRequest(BaseModel):
    """Schema for deleting schedule by direction."""

    start_date: date = Field(..., description="Start date of the source period")
    weeks_to_delete: int = Field(..., description="Number of weeks to delete")
    direction_id: int = Field(..., description="Direction ID")
