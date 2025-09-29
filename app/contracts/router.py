from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contract import ContractCreate, ContractUpdate, Contract
from app.contracts.repository import contract_repository

router = APIRouter()

@router.post("/", response_model=Contract, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db)
):
    """Criar novo contrato"""
    contract_repo = contract_repository(db)
    
    # Verificar se unidade e inquilino existem
    if not contract_repo.unit_exists(contract.unit_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )
    
    if not contract_repo.tenant_exists(contract.tenant_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inquilino não encontrado"
        )
    
    # Verificar se unidade está disponível
    if contract_repo.unit_has_active_contract(contract.unit_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unidade já possui contrato ativo"
        )
    
    db_contract = contract_repo.create(contract)
    return db_contract

@router.get("/", response_model=List[Contract])
async def list_contracts(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    tenant_id: int = None,
    property_id: int = None,
    db: Session = Depends(get_db)
):
    """Listar contratos"""
    contract_repo = contract_repository(db)
    
    filters = {}
    if status:
        filters["status"] = status
    if tenant_id:
        filters["tenant_id"] = tenant_id
    if property_id:
        filters["property_id"] = property_id
    
    contracts = contract_repo.get_multi(skip=skip, limit=limit, **filters)
    return contracts

@router.get("/{contract_id}", response_model=Contract)
async def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """Obter contrato por ID"""
    contract_repo = contract_repository(db)
    contract = contract_repo.get(contract_id)
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    return contract

@router.put("/{contract_id}", response_model=Contract)
async def update_contract(
    contract_id: int,
    contract_update: ContractUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar contrato"""
    contract_repo = contract_repository(db)
    contract = contract_repo.get(contract_id)
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    updated_contract = contract_repo.update(contract_id, contract_update)
    return updated_contract

@router.post("/{contract_id}/renew", response_model=Contract)
async def renew_contract(
    contract_id: int,
    new_end_date: str,
    new_rent_amount: float = None,
    db: Session = Depends(get_db)
):
    """Renovar contrato"""
    contract_repo = contract_repository(db)
    contract = contract_repo.get(contract_id)
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    if contract.status != "ativo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas contratos ativos podem ser renovados"
        )
    
    renewed_contract = contract_repo.renew_contract(
        contract_id, 
        new_end_date, 
        new_rent_amount
    )
    return renewed_contract

@router.post("/{contract_id}/terminate", response_model=Contract)
async def terminate_contract(
    contract_id: int,
    termination_date: str,
    reason: str = None,
    db: Session = Depends(get_db)
):
    """Rescindir contrato"""
    contract_repo = contract_repository(db)
    contract = contract_repo.get(contract_id)
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    if contract.status != "ativo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas contratos ativos podem ser rescindidos"
        )
    
    terminated_contract = contract_repo.terminate_contract(
        contract_id, 
        termination_date, 
        reason
    )
    return terminated_contract

@router.get("/expiring/{days}", response_model=List[Contract])
async def get_expiring_contracts(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Obter contratos que vencem em X dias"""
    contract_repo = contract_repository(db)
    contracts = contract_repo.get_expiring_contracts(days)
    return contracts