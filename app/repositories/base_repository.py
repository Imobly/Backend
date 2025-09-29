from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar, Type, Any
from sqlalchemy.orm import Session
from app.db.base import Base

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Repository base com operações CRUD genéricas"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Buscar entidade por ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Buscar múltiplas entidades com paginação"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Criar nova entidade"""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """Atualizar entidade existente"""
        obj_data = obj_in.dict(exclude_unset=True)
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> bool:
        """Deletar entidade por ID"""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
    
    def count(self, db: Session) -> int:
        """Contar total de entidades"""
        return db.query(self.model).count()