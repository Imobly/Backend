from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from .controller import tenant_controller
from .schemas import TenantCreate, TenantResponse, TenantUpdate

router = APIRouter()


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    """Criar novo inquilino"""
    return tenant_controller(db).create_tenant(db, tenant)


@router.get("/", response_model=List[TenantResponse])
async def list_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar inquilinos"""
    return tenant_controller(db).get_tenants(db, skip=skip, limit=limit)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """Obter inquilino por ID"""
    return tenant_controller(db).get_tenant_by_id(db, tenant_id)


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(tenant_id: int, tenant_update: TenantUpdate, db: Session = Depends(get_db)):
    """Atualizar inquilino"""
    return tenant_controller(db).update_tenant(db, tenant_id, tenant_update)


@router.delete("/{tenant_id}")
async def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """Deletar inquilino"""
    return tenant_controller(db).delete_tenant(db, tenant_id)
