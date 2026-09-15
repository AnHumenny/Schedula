from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class GroupBase(BaseModel):
    """Base schema for group data containing shared fields."""

    name: str = Field(..., max_length=255, description="Name of the group")
    direction_id: int = Field(..., description="ID of the direction the group belongs to")
    description: str | None = Field(None, description="Group description or notes")


class GroupCreate(GroupBase):
    """Schema for creating a new group."""

    profile_id: int | None = Field(None, description="ID of the profile associated with the group")


class GroupUpdate(BaseModel):
    """Schema for updating an existing group."""

    name: str | None = Field(None, max_length=255, description="Name of the group")
    direction_id: int | None = Field(None, description="ID of the direction the group belongs to")
    profile_id: int | None = Field(None, description="ID of the profile associated with the group")
    description: str | None = Field(None, description="Group description or notes")
    is_active: bool | None = Field(None, description="Active status of the group")


class GroupRead(GroupBase):
    """Schema for reading complete group details."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the group")
    is_active: bool = Field(..., description="Active status of the group")
    profile_id: int | None = Field(None, description="ID of the profile associated with the group")
    created_at: datetime = Field(..., description="Timestamp when the group was created")
    updated_at: datetime = Field(..., description="Timestamp when the group was last updated")
    # user_ids: list[int] —  if need list of group