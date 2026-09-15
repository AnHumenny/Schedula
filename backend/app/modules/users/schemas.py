from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modules.users.enums import UserRole


class UserBase(BaseModel):
    """Base schema for user data containing shared fields."""

    email: EmailStr = Field(..., description="Email address of the user")
    username: str = Field(..., description="Unique username of the user")
    role: UserRole = Field(UserRole.USER, description="Role assigned to the user")


class UserCreate(UserBase):
    """Schema for creating a new user account."""

    password: str = Field(..., min_length=8, max_length=128, description="Password for the user account")
    group_id: int | None = Field(None, description="ID of the group the user belongs to")
    profile_id: int | None = Field(None, description="ID of the profile associated with the user")


class UserUpdate(BaseModel):
    """Schema for updating an existing user account."""

    email: EmailStr | None = Field(None, description="Email address of the user")
    username: str | None = Field(None, description="Unique username of the user")
    role: UserRole | None = Field(None, description="Role assigned to the user")
    is_active: bool | None = Field(None, description="Active status of the user account")
    group_id: int | None = Field(None, description="ID of the group the user belongs to")
    profile_id: int | None = Field(None, description="ID of the profile associated with the user")


class UserRead(UserBase):
    """Schema for reading complete user details."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the user")
    is_active: bool = Field(..., description="Active status of the user account")
    group_id: int | None = Field(None, description="ID of the group the user belongs to")
    profile_id: int | None = Field(None, description="ID of the profile associated with the user")
    created_at: datetime = Field(..., description="Timestamp when the user account was created")
    updated_at: datetime = Field(..., description="Timestamp when the user account was last updated")
