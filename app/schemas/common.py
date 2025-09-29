from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime, date
from decimal import Decimal


# Schemas para Dashboard e Analytics
class DashboardMetrics(BaseModel):
    total_properties: int
    occupied_properties: int
    vacant_properties: int
    maintenance_properties: int
    total_tenants: int
    active_tenants: int
    monthly_revenue: Decimal
    pending_payments: int
    overdue_payments: int
    maintenance_requests: int


class RevenueData(BaseModel):
    month: str
    revenue: Decimal
    expenses: Decimal
    profit: Decimal


class OccupancyData(BaseModel):
    property_id: int
    property_name: str
    status: str
    tenant_name: str = None
    rent: Decimal


class PaymentAnalytics(BaseModel):
    total_payments: int
    paid_payments: int
    pending_payments: int
    overdue_payments: int
    total_amount: Decimal
    paid_amount: Decimal
    pending_amount: Decimal
    overdue_amount: Decimal


class ExpenseAnalytics(BaseModel):
    total_expenses: int
    paid_expenses: int
    pending_expenses: int
    total_amount: Decimal
    by_category: Dict[str, Decimal]
    by_property: Dict[str, Decimal]


# Schema para upload de arquivos
class FileUpload(BaseModel):
    filename: str
    content_type: str
    size: int
    url: str


class FileUpload(BaseModel):
    success: bool
    file_id: str
    filename: str
    url: str
    message: str
