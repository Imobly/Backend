from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from .schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from .repository import notification_repository

router = APIRouter()

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """Criar nova notificação"""
    notification_repo = notification_repository(db)
    db_notification = notification_repo.create(notification)
    return db_notification

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    read: bool = None,
    type: str = None,
    db: Session = Depends(get_db)
):
    """Listar notificações"""
    notification_repo = notification_repository(db)
    
    filters = {}
    if read is not None:
        filters["read"] = read
    if type:
        filters["type"] = type
    
    notifications = notification_repo.get_multi(skip=skip, limit=limit, **filters)
    return notifications

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: int, db: Session = Depends(get_db)):
    """Obter notificação por ID"""
    notification_repo = notification_repository(db)
    notification = notification_repo.get(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    return notification

@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Marcar notificação como lida"""
    notification_repo = notification_repository(db)
    notification = notification_repo.get(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    read_notification = notification_repo.mark_as_read(notification_id)
    return read_notification

@router.put("/mark-all-read", response_model=dict)
async def mark_all_as_read(db: Session = Depends(get_db)):
    """Marcar todas as notificações como lidas"""
    notification_repo = notification_repository(db)
    count = notification_repo.mark_all_as_read()
    return {"message": f"{count} notificações marcadas como lidas"}

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """Deletar notificação"""
    notification_repo = notification_repository(db)
    notification = notification_repo.get(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    notification_repo.delete(notification_id)

@router.get("/unread/count", response_model=dict)
async def get_unread_count(db: Session = Depends(get_db)):
    """Obter quantidade de notificações não lidas"""
    notification_repo = notification_repository(db)
    count = notification_repo.get_unread_count()
    return {"unread_count": count}
