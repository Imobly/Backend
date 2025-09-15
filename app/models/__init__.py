# Importar todos os modelos para facilitar o acesso
from .property import Property
from .tenant import Tenant
from .contract import Contract
from .payment import Payment
from .maintenance import Maintenance

__all__ = ["Property", "Tenant", "Contract", "Payment", "Maintenance"]