from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class ContractBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    rent: Decimal = Field(..., gt=0)
    deposit: Decimal = Field(..., ge=0)
    interest_rate: Decimal = Field(..., ge=0)
    fine_rate: Decimal = Field(..., ge=0)
    status: str = Field("active", pattern="^(active|expired|terminated)$")
    document_url: Optional[str] = None

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    rent: Optional[Decimal] = Field(None, gt=0)
    deposit: Optional[Decimal] = Field(None, ge=0)
    interest_rate: Optional[Decimal] = Field(None, ge=0)
    fine_rate: Optional[Decimal] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|expired|terminated)$")
    document_url: Optional[str] = None


class ContractResponse(ContractBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Alias para Response
Contract = ContractResponse


class ContractInDB(Contract):
    pass


# Schema para filtros
class ContractFilter(BaseModel):
    property_id: Optional[int] = None
    tenant_id: Optional[int] = None
    status: Optional[str] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    end_date_from: Optional[date] = None
    end_date_to: Optional[date] = None
