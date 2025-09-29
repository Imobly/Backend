from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, datetime, timedelta
from app.payments.models import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.repositories.base_repository import BaseRepository


class payment_repository(BaseRepository[Payment, PaymentCreate, PaymentUpdate]):
    """Repository para operações com pagamentos"""
    
    def __init__(self):
        super().__init__(Payment)
    
    def get_by_contract(self, db: Session, contract_id: int) -> List[Payment]:
        """Buscar pagamentos por contrato"""
        return db.query(Payment).filter(Payment.contract_id == contract_id).all()
    
    def get_by_tenant(self, db: Session, tenant_id: int) -> List[Payment]:
        """Buscar pagamentos por inquilino"""
        return db.query(Payment).filter(Payment.tenant_id == tenant_id).all()
    
    def get_by_property(self, db: Session, property_id: int) -> List[Payment]:
        """Buscar pagamentos por propriedade"""
        return db.query(Payment).filter(Payment.property_id == property_id).all()
    
    def get_by_status(self, db: Session, status: str) -> List[Payment]:
        """Buscar pagamentos por status"""
        return db.query(Payment).filter(Payment.status == status).all()
    
    def get_overdue_payments(self, db: Session) -> List[Payment]:
        """Buscar pagamentos em atraso"""
        return db.query(Payment).filter(
            Payment.status.in_(["pending", "partial"]),
            Payment.due_date < date.today()
        ).all()
    
    def get_pending_payments(self, db: Session) -> List[Payment]:
        """Buscar pagamentos pendentes"""
        return self.get_by_status(db, "pending")
    
    def get_payments_by_period(
        self, 
        db: Session, 
        start_date: date, 
        end_date: date,
        payment_field: str = "due_date"
    ) -> List[Payment]:
        """Buscar pagamentos por período"""
        if payment_field == "payment_date":
            return db.query(Payment).filter(
                Payment.payment_date.between(start_date, end_date)
            ).all()
        else:
            return db.query(Payment).filter(
                Payment.due_date.between(start_date, end_date)
            ).all()
    
    def update_payment_status(
        self, 
        db: Session, 
        payment_id: int, 
        status: str,
        payment_date: Optional[date] = None,
        payment_method: Optional[str] = None
    ) -> Optional[Payment]:
        """Atualizar status do pagamento"""
        payment_obj = self.get(db, payment_id)
        if payment_obj:
            payment_obj.status = status
            if payment_date:
                payment_obj.payment_date = payment_date
            if payment_method:
                payment_obj.payment_method = payment_method
            db.commit()
            db.refresh(payment_obj)
            return payment_obj
        return None
    
    def calculate_fine(self, db: Session, payment_id: int) -> Optional[Payment]:
        """Calcular multa automaticamente"""
        payment_obj = self.get(db, payment_id)
        if payment_obj and payment_obj.due_date < date.today():
            # Buscar taxa de multa do contrato
            from app.contracts.models import Contract
            contract = db.query(Contract).filter(Contract.id == payment_obj.contract_id).first()
            if contract:
                days_overdue = (date.today() - payment_obj.due_date).days
                fine_rate = float(contract.fine_rate) / 100
                payment_obj.fine_amount = payment_obj.amount * fine_rate
                payment_obj.total_amount = payment_obj.amount + payment_obj.fine_amount
                payment_obj.status = "overdue"
                db.commit()
                db.refresh(payment_obj)
                return payment_obj
        return None


# Instância global do repository
payment_repository = payment_repository()