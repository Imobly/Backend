from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from app.services import tenant_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Tenant])
def get_tenants(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Listar todos os inquilinos"""
    tenants = tenant_service.get_tenants(db, skip=skip, limit=limit)
    return tenants

@router.post("/", response_model=Tenant)
def create_tenant(
    tenant: TenantCreate, 
    db: Session = Depends(get_db)
):
    """Criar novo inquilino"""
    return tenant_service.create_tenant(db=db, tenant=tenant)

@router.get("/{tenant_id}", response_model=Tenant)
def get_tenant(
    tenant_id: int, 
    db: Session = Depends(get_db)
):
    """Obter inquilino por ID"""
    db_tenant = tenant_service.get_tenant(db, tenant_id=tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Inquilino não encontrado")
    return db_tenant

@router.put("/{tenant_id}", response_model=Tenant)
def update_tenant(
    tenant_id: int, 
    tenant: TenantUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar inquilino"""
    db_tenant = tenant_service.update_tenant(db, tenant_id=tenant_id, tenant=tenant)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Inquilino não encontrado")
    return db_tenant

@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int, 
    db: Session = Depends(get_db)
):
    """Deletar inquilino"""
    success = tenant_service.delete_tenant(db, tenant_id=tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inquilino não encontrado")
    return {"message": "Inquilino deletado com sucesso"}