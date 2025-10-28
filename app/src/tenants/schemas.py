from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class EmergencyContact(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=1, max_length=20)
    relationship: str = Field(..., min_length=1, max_length=100)


class TenantDocument(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., pattern="^(identity|contract|other)$")
    url: str


class TenantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=20)
    cpf_cnpj: str = Field(..., min_length=1, max_length=20)
    birth_date: Optional[date] = None
    profession: str = Field(..., min_length=1, max_length=100)
    emergency_contact: Optional[EmergencyContact] = None
    documents: Optional[List[TenantDocument]] = []
    status: str = Field("active", pattern="^(active|inactive)$")


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    cpf_cnpj: Optional[str] = Field(None, min_length=1, max_length=20)
    birth_date: Optional[date] = None
    profession: Optional[str] = Field(None, min_length=1, max_length=100)
    emergency_contact: Optional[EmergencyContact] = None
    documents: Optional[List[TenantDocument]] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive)$")


class TenantResponse(TenantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantInDB(TenantResponse):
    pass


# Schema para filtros
class TenantFilter(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    status: Optional[str] = None
    profession: Optional[str] = None


# Tenant já definido como TenantResponse acima
