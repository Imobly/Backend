from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PropertyBase(BaseModel):
    address: str
    property_type: str
    area: Optional[Decimal] = None
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    description: Optional[str] = None
    monthly_rent: Decimal
    status: Optional[str] = "disponivel"

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    address: Optional[str] = None
    property_type: Optional[str] = None
    area: Optional[Decimal] = None
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    description: Optional[str] = None
    monthly_rent: Optional[Decimal] = None
    status: Optional[str] = None

class Property(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True