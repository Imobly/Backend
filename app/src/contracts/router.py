from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from .schemas import ContractCreate, ContractUpdate, ContractResponse
from .controller import contract_controller

router = APIRouter()

@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db)
):
    """Criar novo contrato"""
    return contract_controller(db).create_contract(db, contract)

@router.get("/", response_model=List[ContractResponse])
async def list_contracts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar contratos"""
    return contract_controller(db).get_contracts(db, skip=skip, limit=limit)

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """Obter contrato por ID"""
    return contract_controller(db).get_contract_by_id(db, contract_id)

@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: int,
    contract_update: ContractUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar contrato"""
    return contract_controller(db).update_contract(db, contract_id, contract_update)

@router.delete("/{contract_id}")
async def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """Deletar contrato"""
    return contract_controller(db).delete_contract(db, contract_id)
