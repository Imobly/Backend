from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.properties.repository import property_repository
from app.properties.schemas import Property, PropertyCreate, PropertyUpdate
from app.db.session import get_db


class property_controller:
    """Controller para gerenciar operações de propriedades"""
    
    def __init__(self):
        self.repository = property_repository
    
    def get_properties(
        self, 
        db: Session,
        skip: int = 0, 
        limit: int = 100,
        property_type: Optional[str] = None,
        status: Optional[str] = None,
        min_rent: Optional[float] = None,
        max_rent: Optional[float] = None,
        min_area: Optional[float] = None,
        max_area: Optional[float] = None
    ) -> List[Property]:
        """Listar propriedades com filtros opcionais"""
        
        # Se houver filtros, usar busca avançada
        if any([property_type, status, min_rent, max_rent, min_area, max_area]):
            return self.repository.search_properties(
                db=db,
                property_type=property_type,
                status=status,
                min_rent=min_rent,
                max_rent=max_rent,
                min_area=min_area,
                max_area=max_area,
                skip=skip,
                limit=limit
            )
        
        # Caso contrário, usar listagem padrão
        return self.repository.get_multi(db, skip=skip, limit=limit)
    
    def get_property_by_id(self, db: Session, property_id: int) -> Property:
        """Obter propriedade por ID"""
        property_obj = self.repository.get(db, property_id)
        if not property_obj:
            raise HTTPException(
                status_code=404, 
                detail="Imóvel não encontrado"
            )
        return property_obj
    
    def create_property(self, db: Session, property_data: PropertyCreate) -> Property:
        """Criar nova propriedade"""
        return self.repository.create(db, obj_in=property_data)
    
    def update_property(
        self, 
        db: Session, 
        property_id: int, 
        property_data: PropertyUpdate
    ) -> Property:
        """Atualizar propriedade existente"""
        property_obj = self.repository.get(db, property_id)
        if not property_obj:
            raise HTTPException(
                status_code=404, 
                detail="Imóvel não encontrado"
            )
        
        return self.repository.update(
            db, db_obj=property_obj, obj_in=property_data
        )
    
    def delete_property(self, db: Session, property_id: int) -> dict:
        """Deletar propriedade"""
        success = self.repository.delete(db, id=property_id)
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Imóvel não encontrado"
            )
        return {"message": "Imóvel deletado com sucesso"}
    
    def get_available_properties(self, db: Session) -> List[Property]:
        """Obter apenas propriedades disponíveis"""
        return self.repository.get_available_properties(db)
    
    def update_property_status(
        self, 
        db: Session, 
        property_id: int, 
        status: str
    ) -> Property:
        """Atualizar apenas o status da propriedade"""
        valid_statuses = ["disponivel", "ocupado", "manutencao"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Status inválido. Use: {', '.join(valid_statuses)}"
            )
        
        property_obj = self.repository.update_status(db, property_id, status)
        if not property_obj:
            raise HTTPException(
                status_code=404,
                detail="Imóvel não encontrado"
            )
        return property_obj


# Instância global do controller
property_controller = property_controller()