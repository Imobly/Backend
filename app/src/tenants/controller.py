from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from .repository import tenant_repository
from .schemas import TenantResponse, TenantCreate, TenantUpdate
from app.db.session import get_db


class tenant_controller:
    """Controller para gerenciar operações de inquilinos"""
    
    def __init__(self):
        self.repository = tenant_repository
    
    def get_tenants(
        self, 
        db: Session,
        skip: int = 0, 
        limit: int = 100,
        name: Optional[str] = None,
        email: Optional[str] = None,
        cpf: Optional[str] = None
    ) -> List[TenantResponse]:
        """Listar inquilinos com filtros opcionais"""
        
        # Se houver filtros, usar busca avançada
        if any([name, email, cpf]):
            return self.repository.search_tenants(
                db=db,
                name=name,
                email=email,
                cpf=cpf,
                skip=skip,
                limit=limit
            )
        
        # Caso contrário, usar listagem padrão
        return self.repository.get_multi(db, skip=skip, limit=limit)
    
    def get_tenant_by_id(self, db: Session, tenant_id: int) -> TenantResponse:
        """Obter inquilino por ID"""
        tenant_obj = self.repository.get(db, tenant_id)
        if not tenant_obj:
            raise HTTPException(
                status_code=404, 
                detail="Inquilino não encontrado"
            )
        return tenant_obj
    
    def get_tenant_by_email(self, db: Session, email: str) -> TenantResponse:
        """Obter inquilino por email"""
        tenant_obj = self.repository.get_by_email(db, email)
        if not tenant_obj:
            raise HTTPException(
                status_code=404, 
                detail="Inquilino não encontrado"
            )
        return tenant_obj
    
    def get_tenant_by_cpf(self, db: Session, cpf: str) -> TenantResponse:
        """Obter inquilino por CPF"""
        tenant_obj = self.repository.get_by_cpf(db, cpf)
        if not tenant_obj:
            raise HTTPException(
                status_code=404, 
                detail="Inquilino não encontrado"
            )
        return tenant_obj
    
    def create_tenant(self, db: Session, tenant_data: TenantCreate) -> TenantResponse:
        """Criar novo inquilino"""
        
        # Verificar se email e CPF são únicos
        validation_errors = self.repository.check_unique_constraints(db, tenant_data)
        if validation_errors:
            raise HTTPException(
                status_code=400,
                detail=validation_errors
            )
        
        return self.repository.create(db, obj_in=tenant_data)
    
    def update_tenant(
        self, 
        db: Session, 
        tenant_id: int, 
        tenant_data: TenantUpdate
    ) -> TenantResponse:
        """Atualizar inquilino existente"""
        tenant_obj = self.repository.get(db, tenant_id)
        if not tenant_obj:
            raise HTTPException(
                status_code=404, 
                detail="Inquilino não encontrado"
            )
        
        # Verificar se email e CPF são únicos (excluindo o próprio registro)
        if hasattr(tenant_data, 'email') and tenant_data.email:
            tenant_create_data = TenantCreate(**tenant_data.dict())
            validation_errors = self.repository.check_unique_constraints(
                db, tenant_create_data, exclude_id=tenant_id
            )
            if validation_errors:
                raise HTTPException(
                    status_code=400,
                    detail=validation_errors
                )
        
        return self.repository.update(
            db, db_obj=tenant_obj, obj_in=tenant_data
        )
    
    def delete_tenant(self, db: Session, tenant_id: int) -> dict:
        """Deletar inquilino"""
        success = self.repository.delete(db, id=tenant_id)
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Inquilino não encontrado"
            )
        return {"message": "Inquilino deletado com sucesso"}
    
    def validate_tenant_exists(self, db: Session, tenant_id: int) -> bool:
        """Validar se inquilino existe (útil para outras operações)"""
        return self.repository.get(db, tenant_id) is not None


# Instância global do controller
tenant_controller = tenant_controller()