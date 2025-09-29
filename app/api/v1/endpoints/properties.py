from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.properties.schemas import Property, PropertyCreate, PropertyUpdate
from app.properties.controller import property_controller
from app.views.response_views import PropertyView
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Property])
def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    property_type: Optional[str] = Query(None, description="Filtrar por tipo de propriedade"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    min_rent: Optional[float] = Query(None, ge=0, description="Valor mínimo do aluguel"),
    max_rent: Optional[float] = Query(None, ge=0, description="Valor máximo do aluguel"),
    min_area: Optional[float] = Query(None, ge=0, description="Área mínima"),
    max_area: Optional[float] = Query(None, ge=0, description="Área máxima"),
    db: Session = Depends(get_db)
):
    """Listar propriedades com filtros opcionais"""
    properties = property_controller.get_properties(
        db=db,
        skip=skip,
        limit=limit,
        property_type=property_type,
        status=status,
        min_rent=min_rent,
        max_rent=max_rent,
        min_area=min_area,
        max_area=max_area
    )
    return properties

@router.get("/available")
def get_available_properties(db: Session = Depends(get_db)):
    """Listar apenas propriedades disponíveis"""
    properties = property_controller.get_available_properties(db)
    return PropertyView.list_response(properties, "Propriedades disponíveis listadas com sucesso")

@router.post("/", response_model=Property)
def create_property(
    property: PropertyCreate, 
    db: Session = Depends(get_db)
):
    """Criar nova propriedade"""
    new_property = property_controller.create_property(db=db, property_data=property)
    return new_property

@router.get("/{property_id}")
def get_property(
    property_id: int, 
    db: Session = Depends(get_db)
):
    """Obter propriedade por ID"""
    property_obj = property_controller.get_property_by_id(db, property_id=property_id)
    return PropertyView.detail_response(property_obj)

@router.put("/{property_id}")
def update_property(
    property_id: int, 
    property: PropertyUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar propriedade"""
    updated_property = property_controller.update_property(
        db, property_id=property_id, property_data=property
    )
    return PropertyView.updated_response(updated_property)

@router.patch("/{property_id}/status")
def update_property_status(
    property_id: int,
    status: str = Query(..., description="Novo status da propriedade"),
    db: Session = Depends(get_db)
):
    """Atualizar apenas o status da propriedade"""
    updated_property = property_controller.update_property_status(
        db, property_id=property_id, status=status
    )
    return PropertyView.status_updated_response(updated_property)

@router.delete("/{property_id}")
def delete_property(
    property_id: int, 
    db: Session = Depends(get_db)
):
    """Deletar propriedade"""
    property_controller.delete_property(db, property_id=property_id)
    return PropertyView.deleted_response()