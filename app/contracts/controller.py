from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from app.contracts.repository import contract_repository
from app.payments.repository import payment_repository
from app.schemas.contract import Contract, ContractCreate, ContractUpdate


class contract_controller:
    """Controller para gerenciar operações de contratos"""
    
    def __init__(self):
        self.repository = contract_repository
        self.payment_repository = payment_repository
    
    def get_contracts(
        self, 
        db: Session,
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        property_id: Optional[int] = None,
        tenant_id: Optional[int] = None
    ) -> List[Contract]:
        """Listar contratos com filtros"""
        if status:
            contracts = self.repository.get_by_status(db, status)
        elif property_id:
            contracts = self.repository.get_by_property(db, property_id)
        elif tenant_id:
            contracts = self.repository.get_by_tenant(db, tenant_id)
        else:
            contracts = self.repository.get_multi(db, skip=skip, limit=limit)
        
        return contracts[skip:skip+limit] if not any([status, property_id, tenant_id]) else contracts
    
    def get_contract_by_id(self, db: Session, contract_id: int) -> Contract:
        """Obter contrato por ID"""
        contract_obj = self.repository.get(db, contract_id)
        if not contract_obj:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        return contract_obj
    
    def create_contract(self, db: Session, contract_data: ContractCreate) -> Contract:
        """Criar novo contrato"""
        # Verificar se propriedade está disponível no período
        if not self.repository.check_property_availability(
            db, contract_data.property_id, contract_data.start_date, contract_data.end_date
        ):
            raise HTTPException(
                status_code=400, 
                detail="Propriedade não disponível no período especificado"
            )
        
        return self.repository.create(db, obj_in=contract_data)
    
    def update_contract(
        self, 
        db: Session, 
        contract_id: int, 
        contract_data: ContractUpdate
    ) -> Contract:
        """Atualizar contrato"""
        contract_obj = self.repository.get(db, contract_id)
        if not contract_obj:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
        return self.repository.update(db, db_obj=contract_obj, obj_in=contract_data)
    
    def delete_contract(self, db: Session, contract_id: int) -> dict:
        """Deletar contrato"""
        success = self.repository.delete(db, id=contract_id)
        if not success:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        return {"message": "Contrato deletado com sucesso"}
    
    def get_expiring_contracts(self, db: Session, days_ahead: int = 30) -> List[Contract]:
        """Obter contratos que vencem em breve"""
        return self.repository.get_expiring_contracts(db, days_ahead)
    
    def get_active_contracts(self, db: Session) -> List[Contract]:
        """Obter contratos ativos"""
        return self.repository.get_active_contracts(db)
    
    def renew_contract(
        self, 
        db: Session, 
        contract_id: int, 
        new_end_date: date,
        new_rent: Optional[float] = None
    ) -> Contract:
        """Renovar contrato"""
        contract_obj = self.repository.renew_contract(db, contract_id, new_end_date, new_rent)
        if not contract_obj:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        return contract_obj


# Instância global do controller
contract_controller = contract_controller()