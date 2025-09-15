from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate
from datetime import datetime

def get_property(db: Session, property_id: int) -> Optional[Property]:
    """Obter propriedade por ID"""
    return db.query(Property).filter(Property.id == property_id).first()

def get_properties(db: Session, skip: int = 0, limit: int = 100) -> List[Property]:
    """Listar propriedades com paginação"""
    return db.query(Property).offset(skip).limit(limit).all()

def create_property(db: Session, property: PropertyCreate) -> Property:
    """Criar nova propriedade"""
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, property_id: int, property: PropertyUpdate) -> Optional[Property]:
    """Atualizar propriedade existente"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property:
        update_data = property.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_property, field, value)
        db_property.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int) -> bool:
    """Deletar propriedade"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
        return True
    return False