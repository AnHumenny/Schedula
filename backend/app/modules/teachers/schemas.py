from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TeacherBase(BaseModel):
    """Base schema for teacher data containing shared fields."""

    fullname: str = Field(..., max_length=255, description="Full name of the teacher")
    description: str | None = Field(None, description="Teacher description or notes")


class TeacherCreate(TeacherBase):
    """Schema for creating a new teacher."""

    discipline_ids: list[int] = Field(
        default_factory=list, description="List of discipline IDs the teacher can teach"
    )


class TeacherUpdate(BaseModel):
    """Schema for updating an existing teacher."""

    fullname: str | None = Field(None, max_length=255, description="Full name of the teacher")
    description: str | None = Field(None, description="Teacher description or notes")
    is_active: bool | None = Field(None, description="Active status of the teacher")
    discipline_ids: list[int] | None = Field(
        None, description="List of discipline IDs the teacher can teach"
    )


class TeacherRead(TeacherBase):
    """Schema for reading complete teacher details."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the teacher")
    is_active: bool = Field(..., description="Active status of the teacher")
    created_at: datetime = Field(..., description="Timestamp when the teacher was created")
    updated_at: datetime = Field(..., description="Timestamp when the teacher was last updated")
    discipline_ids: list[int] = Field(
        default_factory=list, description="List of discipline IDs the teacher can teach"
    )


class TeacherShort(BaseModel):
    """Compact schema for nested representations of a teacher."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the teacher")
    fullname: str = Field(..., description="Full name of the teacher")
