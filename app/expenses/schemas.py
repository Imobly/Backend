from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date as date_type
from decimal import Decimal


class ExpenseBase(BaseModel):
    type: str = Field(..., pattern="^(expense|maintenance)$")
    category: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    date: date_type
    property_id: int
    status: str = Field(..., pattern="^(pending|paid|scheduled)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    vendor: Optional[str] = Field(None, max_length=255)
    receipt: Optional[str] = None  # URL do comprovante
    notes: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    type: Optional[str] = Field(None, pattern="^(expense|maintenance)$")
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(None, gt=0)
    date: Optional[date_type] = None
    status: Optional[str] = Field(None, pattern="^(pending|paid|scheduled)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    vendor: Optional[str] = Field(None, max_length=255)
    receipt: Optional[str] = None
    notes: Optional[str] = None


class Expense(ExpenseBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Alias para Response
Expense = Expense


class ExpenseInDB(Expense):
    pass


# Schema para filtros
class ExpenseFilter(BaseModel):
    type: Optional[str] = None
    category: Optional[str] = None
    property_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    date_from: Optional[date_type] = None
    date_to: Optional[date_type] = None
    vendor: Optional[str] = None


# Schema para categorias
class ExpenseCategory(BaseModel):
    name: str
    type: str  # expense ou maintenance
