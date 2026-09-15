from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProfileBase(BaseModel):
    """Base schema for profile data containing shared fields."""

    name: str = Field(..., max_length=255, description="Profile name")
    description: str | None = Field(None, description="Profile description")


class ProfileCreate(ProfileBase):
    """Schema for creating a new profile."""

    pass


class ProfileUpdate(BaseModel):
    """Schema for updating an existing profile."""

    name: str | None = Field(None, max_length=255, description="Profile name")
    description: str | None = Field(None, description="Profile description")
    is_active: bool | None = Field(None, description="Active status of the profile")


class ProfileRead(ProfileBase):
    """Schema for reading complete profile details."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the profile")
    is_active: bool = Field(..., description="Active status of the profile")
    created_at: datetime = Field(..., description="Timestamp when the profile was created")
    updated_at: datetime = Field(..., description="Timestamp when the profile was last updated")


class ProfileShort(BaseModel):
    """Compact schema for nested representations, such as in ScheduleItemRead."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the profile")
    name: str = Field(..., description="Profile name")
