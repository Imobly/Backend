from typing import Any, Dict

from sqlalchemy.orm import Session

from app.src.contracts.repository import ContractRepository
from app.src.payments.repository import PaymentRepository
from app.src.properties.repository import PropertyRepository
from app.src.tenants.repository import TenantRepository


class DashboardController:
    """Controller para gerenciar operações do dashboard"""

    def __init__(self, db: Session):
        self.db = db
        self.property_repo = PropertyRepository(db)
        self.contract_repo = ContractRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.tenant_repo = TenantRepository(db)

    def get_overview(self, db: Session) -> Dict[str, Any]:
        """Obter visão geral do dashboard"""
        # Contar propriedades
        total_properties = len(self.property_repo.get_multi(db, skip=0, limit=10000))

        # Contar inquilinos
        total_tenants = len(self.tenant_repo.get_multi(db, skip=0, limit=10000))

        # Contar contratos ativos
        active_contracts = len(self.contract_repo.get_active_contracts(db))

        # Estatísticas de pagamentos
        pending_payments = len(self.payment_repo.get_pending_payments(db))
        overdue_payments = len(self.payment_repo.get_overdue_payments(db))

        return {
            "total_properties": total_properties,
            "total_tenants": total_tenants,
            "active_contracts": active_contracts,
            "pending_payments": pending_payments,
            "overdue_payments": overdue_payments,
            "occupancy_rate": (active_contracts / max(total_properties, 1)) * 100,
        }

    def get_financial_summary(self, db: Session) -> Dict[str, Any]:
        """Obter resumo financeiro"""
        # Total de receitas esperadas
        total_rent = self.payment_repo.get_total_monthly_rent(db)

        # Pagamentos recebidos no mês
        payments_received = self.payment_repo.get_monthly_payments_received(db)

        # Inadimplência
        overdue_amount = self.payment_repo.get_overdue_amount(db)

        return {
            "expected_monthly_revenue": total_rent,
            "payments_received": payments_received,
            "overdue_amount": overdue_amount,
            "collection_rate": (
                ((payments_received / max(total_rent, 1)) * 100) if total_rent > 0 else 0
            ),
        }

    def get_recent_activities(self, db: Session) -> Dict[str, Any]:
        """Obter atividades recentes"""
        # Contratos recentes
        recent_contracts = self.contract_repo.get_recent_contracts(db, limit=5)

        # Pagamentos recentes
        recent_payments = self.payment_repo.get_recent_payments(db, limit=5)

        return {"recent_contracts": recent_contracts, "recent_payments": recent_payments}


# Controller class ready for use
