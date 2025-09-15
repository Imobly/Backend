# Importar todos os schemas para facilitar o acesso
from .property import Property, PropertyCreate, PropertyUpdate
from .tenant import Tenant, TenantCreate, TenantUpdate

__all__ = [
    "Property", "PropertyCreate", "PropertyUpdate",
    "Tenant", "TenantCreate", "TenantUpdate"
]