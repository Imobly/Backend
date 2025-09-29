from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from app.tenants.controller import tenant_controller
from app.views.response_views import TenantView
from app.db.session import get_db

router = APIRouter()

@router.get("/")
def get_tenants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = Query(None, description="Filtrar por nome"),
    email: Optional[str] = Query(None, description="Filtrar por email"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF"),
    db: Session = Depends(get_db)
):
    """Listar inquilinos com filtros opcionais"""
    tenants = tenant_controller.get_tenants(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        email=email,
        cpf=cpf
    )
    return TenantView.list_response(tenants)

@router.post("/")
def create_tenant(
    tenant: TenantCreate, 
    db: Session = Depends(get_db)
):
    """Criar novo inquilino"""
    new_tenant = tenant_controller.create_tenant(db=db, tenant_data=tenant)
    return TenantView.created_response(new_tenant)

@router.get("/{tenant_id}")
def get_tenant(
    tenant_id: int, 
    db: Session = Depends(get_db)
):
    """Obter inquilino por ID"""
    tenant_obj = tenant_controller.get_tenant_by_id(db, tenant_id=tenant_id)
    return TenantView.detail_response(tenant_obj)

@router.get("/by-email/{email}")
def get_tenant_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Obter inquilino por email"""
    tenant_obj = tenant_controller.get_tenant_by_email(db, email=email)
    return TenantView.detail_response(tenant_obj)

@router.get("/by-cpf/{cpf}")
def get_tenant_by_cpf(
    cpf: str,
    db: Session = Depends(get_db)
):
    """Obter inquilino por CPF"""
    tenant_obj = tenant_controller.get_tenant_by_cpf(db, cpf=cpf)
    return TenantView.detail_response(tenant_obj)

@router.put("/{tenant_id}")
def update_tenant(
    tenant_id: int, 
    tenant: TenantUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar inquilino"""
    updated_tenant = tenant_controller.update_tenant(
        db, tenant_id=tenant_id, tenant_data=tenant
    )
    return TenantView.updated_response(updated_tenant)

@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int, 
    db: Session = Depends(get_db)
):
    """Deletar inquilino"""
    tenant_controller.delete_tenant(db, tenant_id=tenant_id)
    return TenantView.deleted_response()