from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from .repository import payment_repository
from app.src.contracts.repository import contract_repository
from .schemas import PaymentResponse, PaymentCreate, PaymentUpdate, PaymentBulkCreate


class payment_controller:
    """Controller para gerenciar operações de pagamentos"""
    
    def __init__(self):
        self.repository = payment_repository
        self.contract_repository = contract_repository
    
    def get_payments(
        self, 
        db: Session,
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        property_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        contract_id: Optional[int] = None
    ) -> List[PaymentResponse]:
        """Listar pagamentos com filtros"""
        if status:
            payments = self.repository.get_by_status(db, status)
        elif property_id:
            payments = self.repository.get_by_property(db, property_id)
        elif tenant_id:
            payments = self.repository.get_by_tenant(db, tenant_id)
        elif contract_id:
            payments = self.repository.get_by_contract(db, contract_id)
        else:
            payments = self.repository.get_multi(db, skip=skip, limit=limit)
        
        return payments[skip:skip+limit] if not any([status, property_id, tenant_id, contract_id]) else payments
    
    def create_payment(self, db: Session, payment_data: PaymentCreate) -> PaymentResponse:
        """Criar novo pagamento"""
        return self.repository.create(db, obj_in=payment_data)
    
    def create_bulk_payments(self, db: Session, bulk_data: PaymentBulkCreate) -> List[PaymentResponse]:
        """Criar pagamentos em lote para um contrato"""
        contract = self.contract_repository.get(db, bulk_data.contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
        payments = []
        current_date = bulk_data.start_date
        
        for month in range(bulk_data.months):
            payment_data = PaymentCreate(
                property_id=contract.property_id,
                tenant_id=contract.tenant_id,
                contract_id=bulk_data.contract_id,
                due_date=current_date,
                amount=bulk_data.amount,
                total_amount=bulk_data.amount,
                status="pending"
            )
            payment = self.repository.create(db, obj_in=payment_data)
            payments.append(payment)
            current_date = current_date + relativedelta(months=1)
        
        return payments
    
    def update_payment(
        self, 
        db: Session, 
        payment_id: int, 
        payment_data: PaymentUpdate
    ) -> PaymentResponse:
        """Atualizar pagamento"""
        payment_obj = self.repository.get(db, payment_id)
        if not payment_obj:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        return self.repository.update(db, db_obj=payment_obj, obj_in=payment_data)
    
    def process_payment(
        self, 
        db: Session, 
        payment_id: int,
        payment_method: str,
        payment_date: Optional[date] = None
    ) -> PaymentResponse:
        """Processar pagamento"""
        if not payment_date:
            payment_date = date.today()
        
        payment_obj = self.repository.update_payment_status(
            db, payment_id, "paid", payment_date, payment_method
        )
        if not payment_obj:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        return payment_obj
    
    def get_overdue_payments(self, db: Session) -> List[PaymentResponse]:
        """Obter pagamentos em atraso"""
        return self.repository.get_overdue_payments(db)
    
    def get_pending_payments(self, db: Session) -> List[PaymentResponse]:
        """Obter pagamentos pendentes"""
        return self.repository.get_pending_payments(db)
    
    def calculate_fines(self, db: Session) -> int:
        """Calcular multas para pagamentos em atraso"""
        overdue_payments = self.repository.get_overdue_payments(db)
        count = 0
        
        for payment in overdue_payments:
            if payment.fine_amount == 0:  # Só calcular se ainda não foi calculada
                self.repository.calculate_fine(db, payment.id)
                count += 1
        
        return count


# Instância global do controller
payment_controller = payment_controller()
