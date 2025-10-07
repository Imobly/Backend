from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from .schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from .controller import notification_controller

router = APIRouter()

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """Criar nova notificação"""
    return notification_controller(db).create_notification(db, notification)

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar notificações"""
    return notification_controller(db).get_notifications(db, skip=skip, limit=limit)

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: int, db: Session = Depends(get_db)):
    """Obter notificação por ID"""
    return notification_controller(db).get_notification_by_id(db, notification_id)

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar notificação"""
    return notification_controller(db).update_notification(db, notification_id, notification_update)

@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """Deletar notificação"""
    return notification_controller(db).delete_notification(db, notification_id)
