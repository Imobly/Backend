from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class PaymentBase(BaseModel):
    property_id: int
    tenant_id: int
    contract_id: int
    due_date: date
    payment_date: Optional[date] = None
    amount: Decimal = Field(..., gt=0)
    fine_amount: Decimal = Field(0, ge=0)
    total_amount: Decimal = Field(..., gt=0)
    status: str = Field(..., pattern="^(pending|paid|overdue|partial)$")
    payment_method: Optional[str] = Field(None, pattern="^(cash|transfer|pix|check|card)$")
    description: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    due_date: Optional[date] = None
    payment_date: Optional[date] = None
    amount: Optional[Decimal] = Field(None, gt=0)
    fine_amount: Optional[Decimal] = Field(None, ge=0)
    total_amount: Optional[Decimal] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(pending|paid|overdue|partial)$")
    payment_method: Optional[str] = Field(None, pattern="^(cash|transfer|pix|check|card)$")
    description: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Alias para Response
Payment = PaymentResponse


class PaymentInDB(PaymentResponse):
    pass


# Schema para filtros
class PaymentFilter(BaseModel):
    property_id: Optional[int] = None
    tenant_id: Optional[int] = None
    contract_id: Optional[int] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    payment_date_from: Optional[date] = None
    payment_date_to: Optional[date] = None


# Schema para pagamentos em lote
class PaymentBulkCreate(BaseModel):
    contract_id: int
    months: int = Field(..., gt=0, le=12)
    start_date: date
    amount: Decimal = Field(..., gt=0)
