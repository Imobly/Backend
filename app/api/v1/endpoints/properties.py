from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.property import Property, PropertyCreate, PropertyUpdate
from app.services import property_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Property])
def get_properties(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Listar todas as propriedades"""
    properties = property_service.get_properties(db, skip=skip, limit=limit)
    return properties

@router.post("/", response_model=Property)
def create_property(
    property: PropertyCreate, 
    db: Session = Depends(get_db)
):
    """Criar nova propriedade"""
    return property_service.create_property(db=db, property=property)

@router.get("/{property_id}", response_model=Property)
def get_property(
    property_id: int, 
    db: Session = Depends(get_db)
):
    """Obter propriedade por ID"""
    db_property = property_service.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return db_property

@router.put("/{property_id}", response_model=Property)
def update_property(
    property_id: int, 
    property: PropertyUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar propriedade"""
    db_property = property_service.update_property(db, property_id=property_id, property=property)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return db_property

@router.delete("/{property_id}")
def delete_property(
    property_id: int, 
    db: Session = Depends(get_db)
):
    """Deletar propriedade"""
    success = property_service.delete_property(db, property_id=property_id)
    if not success:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return {"message": "Imóvel deletado com sucesso"}