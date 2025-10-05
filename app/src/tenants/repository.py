from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Tenant
from .schemas import TenantCreate, TenantUpdate
from app.db.base_repository import BaseRepository


class tenant_repository(BaseRepository[Tenant, TenantCreate, TenantUpdate]):
    """Repository para operações com inquilinos"""
    
    def __init__(self):
        super().__init__(Tenant)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Tenant]:
        """Buscar inquilino por email"""
        return db.query(Tenant).filter(Tenant.email == email).first()
    
    def get_by_cpf(self, db: Session, cpf: str) -> Optional[Tenant]:
        """Buscar inquilino por CPF"""
        return db.query(Tenant).filter(Tenant.cpf == cpf).first()
    
    def get_by_phone(self, db: Session, phone: str) -> Optional[Tenant]:
        """Buscar inquilino por telefone"""
        return db.query(Tenant).filter(Tenant.phone == phone).first()
    
    def search_tenants(
        self,
        db: Session,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        cpf: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Tenant]:
        """Buscar inquilinos com filtros"""
        query = db.query(Tenant)
        
        if name:
            query = query.filter(Tenant.name.ilike(f"%{name}%"))
        
        if email:
            query = query.filter(Tenant.email.ilike(f"%{email}%"))
        
        if cpf:
            query = query.filter(Tenant.cpf == cpf)
        
        return query.offset(skip).limit(limit).all()
    
    def check_unique_constraints(self, db: Session, tenant_data: TenantCreate, exclude_id: Optional[int] = None) -> dict:
        """Verificar se email e CPF são únicos"""
        errors = {}
        
        # Verificar email único
        email_query = db.query(Tenant).filter(Tenant.email == tenant_data.email)
        if exclude_id:
            email_query = email_query.filter(Tenant.id != exclude_id)
        
        if email_query.first():
            errors["email"] = "Email já está em uso"
        
        # Verificar CPF único
        cpf_query = db.query(Tenant).filter(Tenant.cpf == tenant_data.cpf)
        if exclude_id:
            cpf_query = cpf_query.filter(Tenant.id != exclude_id)
        
        if cpf_query.first():
            errors["cpf"] = "CPF já está em uso"
        
        return errors


# Instância global do repository
tenant_repository = tenant_repository()