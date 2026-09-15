from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BuildingBase(BaseModel):
    """Shared fields for building create and read schemas."""
    name: str = Field(..., max_length=255, description="Name of the building")
    address: str = Field(..., max_length=500, description="Physical address of the building")
    description: str | None = Field(None, description="Building description or notes")


class BuildingCreate(BuildingBase):
    """Schema for creating a new building."""
    pass


class BuildingUpdate(BaseModel):
    """Schema for partial update of a building."""
    name: str | None = Field(None, max_length=255, description="Name of the building")
    address: str | None = Field(None, max_length=500, description="Physical address of the building")
    description: str | None = Field(None, description="Building description or notes")
    is_active: bool | None = Field(None, description="Active status of the building")


class BuildingRead(BuildingBase):
    """Schema for reading a building including metadata."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the building")
    is_active: bool = Field(..., description="Active status of the building")
    created_at: datetime = Field(..., description="Timestamp when the building was created")
    updated_at: datetime = Field(..., description="Timestamp when the building was last updated")


class BuildingShort(BaseModel):
    """Minimal building schema for nested responses (e.g. in RoomRead)."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier of the building")
    name: str = Field(..., description="Name of the building")
    address: str = Field(..., description="Physical address of the building")
