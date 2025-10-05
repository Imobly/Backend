from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from .schemas import UnitCreate, UnitUpdate, UnitResponse
from .repository import unit_repository

router = APIRouter()

@router.post("/", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
async def create_unit(
    unit: UnitCreate,
    db: Session = Depends(get_db)
):
    """Criar nova unidade"""
    unit_repo = unit_repository(db)
    
    # Verificar se a propriedade existe
    if not unit_repo.property_exists(unit.property_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propriedade não encontrada"
        )
    
    # Verificar se já existe unidade com mesmo número na propriedade
    if unit_repo.get_by_number_and_property(unit.unit_number, unit.property_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma unidade com este número nesta propriedade"
        )
    
    db_unit = unit_repo.create(unit)
    return db_unit

@router.get("/", response_model=List[UnitResponse])
async def list_units(
    skip: int = 0,
    limit: int = 100,
    property_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Listar unidades"""
    unit_repo = unit_repository(db)
    
    filters = {}
    if property_id:
        filters["property_id"] = property_id
    if status:
        filters["status"] = status
    
    units = unit_repo.get_multi(skip=skip, limit=limit, **filters)
    return units

@router.get("/{unit_id}", response_model=UnitResponse)
async def get_unit(unit_id: int, db: Session = Depends(get_db)):
    """Obter unidade por ID"""
    unit_repo = unit_repository(db)
    unit = unit_repo.get(unit_id)
    
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )
    
    return unit

@router.put("/{unit_id}", response_model=UnitResponse)
async def update_unit(
    unit_id: int,
    unit_update: UnitUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar unidade"""
    unit_repo = unit_repository(db)
    unit = unit_repo.get(unit_id)
    
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )
    
    # Verificar conflito de número se está sendo alterado
    if unit_update.unit_number and unit_update.unit_number != unit.unit_number:
        existing = unit_repo.get_by_number_and_property(
            unit_update.unit_number, 
            unit.property_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma unidade com este número nesta propriedade"
            )
    
    updated_unit = unit_repo.update(unit_id, unit_update)
    return updated_unit

@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    """Deletar unidade"""
    unit_repo = unit_repository(db)
    unit = unit_repo.get(unit_id)
    
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )
    
    # Verificar se tem contratos ativos
    if unit_repo.has_active_contracts(unit_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar unidade com contratos ativos"
        )
    
    unit_repo.delete(unit_id)

@router.get("/property/{property_id}/available", response_model=List[UnitResponse])
async def get_available_units(
    property_id: int,
    db: Session = Depends(get_db)
):
    """Obter unidades disponíveis de uma propriedade"""
    unit_repo = unit_repository(db)
    units = unit_repo.get_available_by_property(property_id)
    return units
