from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DirectionBase(BaseModel):
    """Shared fields for direction create and read schemas."""
    name: str = Field(..., max_length=255, description="Name of the direction")
    academic_year: str = Field(..., max_length=50, description="Academic year for the direction")
    description: str | None = Field(None, description="Direction description or notes")


class DirectionCreate(DirectionBase):
    """Schema for creating a new direction."""
    pass


class DirectionRead(DirectionBase):
    """Schema for reading a direction including metadata."""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Unique identifier of the direction")
    is_active: bool = Field(..., description="Active status of the direction")
    created_at: datetime = Field(..., description="Timestamp when the direction was created")
    updated_at: datetime = Field(..., description="Timestamp when the direction was last updated")


class DirectionUpdate(BaseModel):
    """Schema for partial update of a direction."""
    name: str | None = Field(None, max_length=255, description="Name of the direction")
    academic_year: str | None = Field(None, max_length=50, description="Academic year for the direction")
    description: str | None = Field(None, description="Direction description or notes")
    is_active: bool | None = Field(None, description="Active status of the direction")
