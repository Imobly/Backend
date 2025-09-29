from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, datetime, timedelta
from app.contracts.models import Contract
from app.schemas.contract import ContractCreate, ContractUpdate
from app.repositories.base_repository import BaseRepository


class contract_repository(BaseRepository[Contract, ContractCreate, ContractUpdate]):
    """Repository para operações com contratos"""
    
    def __init__(self):
        super().__init__(Contract)
    
    def get_by_property(self, db: Session, property_id: int) -> List[Contract]:
        """Buscar contratos por propriedade"""
        return db.query(Contract).filter(Contract.property_id == property_id).all()
    
    def get_by_tenant(self, db: Session, tenant_id: int) -> List[Contract]:
        """Buscar contratos por inquilino"""
        return db.query(Contract).filter(Contract.tenant_id == tenant_id).all()
    
    def get_by_status(self, db: Session, status: str) -> List[Contract]:
        """Buscar contratos por status"""
        return db.query(Contract).filter(Contract.status == status).all()
    
    def get_active_contracts(self, db: Session) -> List[Contract]:
        """Buscar apenas contratos ativos"""
        return self.get_by_status(db, "active")
    
    def get_expiring_contracts(self, db: Session, days_ahead: int = 30) -> List[Contract]:
        """Buscar contratos que vencem nos próximos X dias"""
        future_date = date.today() + timedelta(days=days_ahead)
        return db.query(Contract).filter(
            Contract.status == "active",
            Contract.end_date <= future_date,
            Contract.end_date >= date.today()
        ).all()
    
    def get_expired_contracts(self, db: Session) -> List[Contract]:
        """Buscar contratos vencidos"""
        return db.query(Contract).filter(
            Contract.end_date < date.today(),
            Contract.status == "active"
        ).all()
    
    def get_current_contract_for_property(self, db: Session, property_id: int) -> Optional[Contract]:
        """Buscar contrato ativo atual de uma propriedade"""
        return db.query(Contract).filter(
            Contract.property_id == property_id,
            Contract.status == "active",
            Contract.start_date <= date.today(),
            Contract.end_date >= date.today()
        ).first()
    
    def get_current_contract_for_tenant(self, db: Session, tenant_id: int) -> Optional[Contract]:
        """Buscar contrato ativo atual de um inquilino"""
        return db.query(Contract).filter(
            Contract.tenant_id == tenant_id,
            Contract.status == "active",
            Contract.start_date <= date.today(),
            Contract.end_date >= date.today()
        ).first()
    
    def check_property_availability(
        self, 
        db: Session, 
        property_id: int, 
        start_date: date, 
        end_date: date,
        exclude_contract_id: Optional[int] = None
    ) -> bool:
        """Verificar se propriedade está disponível no período"""
        query = db.query(Contract).filter(
            Contract.property_id == property_id,
            Contract.status == "active",
            or_(
                and_(Contract.start_date <= start_date, Contract.end_date >= start_date),
                and_(Contract.start_date <= end_date, Contract.end_date >= end_date),
                and_(Contract.start_date >= start_date, Contract.end_date <= end_date)
            )
        )
        
        if exclude_contract_id:
            query = query.filter(Contract.id != exclude_contract_id)
        
        return query.first() is None
    
    def update_status(self, db: Session, contract_id: int, status: str) -> Optional[Contract]:
        """Atualizar apenas o status do contrato"""
        contract_obj = self.get(db, contract_id)
        if contract_obj:
            contract_obj.status = status
            db.commit()
            db.refresh(contract_obj)
            return contract_obj
        return None
    
    def renew_contract(
        self, 
        db: Session, 
        contract_id: int, 
        new_end_date: date,
        new_rent: Optional[float] = None
    ) -> Optional[Contract]:
        """Renovar contrato"""
        contract_obj = self.get(db, contract_id)
        if contract_obj:
            contract_obj.end_date = new_end_date
            if new_rent:
                contract_obj.rent = new_rent
            db.commit()
            db.refresh(contract_obj)
            return contract_obj
        return None


# Instância global do repository
contract_repository = contract_repository()