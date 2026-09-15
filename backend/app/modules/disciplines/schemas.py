from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DisciplineBase(BaseModel):
    """Shared fields for discipline create and read schemas."""
    name: str = Field(..., max_length=255, description="Name of the discipline")
    description: str | None = Field(None, description="Discipline description or notes")


class DisciplineCreate(DisciplineBase):
    """Schema for creating a new discipline."""
    pass


class DisciplineUpdate(BaseModel):
    """Schema for partial update of a discipline."""
    name: str | None = Field(None, max_length=255, description="Name of the discipline")
    description: str | None = Field(None, description="Discipline description or notes")
    is_active: bool | None = Field(None, description="Active status of the discipline")


class DisciplineRead(DisciplineBase):
    """Schema for reading a discipline including metadata."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the discipline")
    is_active: bool = Field(..., description="Active status of the discipline")
    created_at: datetime = Field(..., description="Timestamp when the discipline was created")
    updated_at: datetime = Field(..., description="Timestamp when the discipline was last updated")


class DisciplineShort(BaseModel):
    """Minimal discipline schema with id and name only."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the discipline")
    name: str = Field(..., description="Name of the discipline")
