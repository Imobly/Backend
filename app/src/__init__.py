"""
Source module - Todos os módulos de domínio da aplicação
"""

# Importar todos os módulos para facilitar acesso
from . import properties
from . import tenants
from . import contracts
from . import payments
from . import expenses
from . import notifications
from . import units
from . import dashboard

__all__ = [
    "properties",
    "tenants", 
    "contracts",
    "payments",
    "expenses", 
    "notifications",
    "units",
    "dashboard"
]