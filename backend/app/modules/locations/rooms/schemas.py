from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class RoomBase(BaseModel):
    """Base schema for room data containing shared fields."""

    number: str = Field(..., max_length=100, description="Room number or name")
    description: str | None = Field(None, description="Room description")


class RoomCreate(RoomBase):
    """Schema for creating a new room."""

    building_id: int = Field(..., description="ID of the building containing the room")


class RoomUpdate(BaseModel):
    """Schema for updating an existing room."""

    building_id: int | None = Field(None, description="ID of the building containing the room")
    number: str | None = Field(None, max_length=100, description="Room number or name")
    description: str | None = Field(None, description="Room description")
    is_active: bool | None = Field(None, description="Active status of the room")


class RoomRead(RoomBase):
    """Schema for reading complete room details."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the room")
    building_id: int = Field(..., description="ID of the building containing the room")
    is_active: bool = Field(..., description="Active status of the room")
    created_at: datetime = Field(..., description="Timestamp when the room was created")
    updated_at: datetime = Field(..., description="Timestamp when the room was last updated")


class RoomShort(BaseModel):
    """Compact schema for nested representations, such as in ScheduleItemRead."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the room")
    building_id: int = Field(..., description="ID of the building containing the room")
    number: str = Field(..., description="Room number or name")
    description: str | None = Field(None, description="Room description")
