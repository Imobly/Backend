from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from .controller import payment_controller
from .schemas import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Criar novo pagamento"""
    return payment_controller(db).create_payment(db, payment)


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar pagamentos"""
    return payment_controller(db).get_payments(db, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Obter pagamento por ID"""
    return payment_controller(db).get_payment_by_id(db, payment_id)


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_db)
):
    """Atualizar pagamento"""
    return payment_controller(db).update_payment(db, payment_id, payment_update)


@router.delete("/{payment_id}")
async def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Deletar pagamento"""
    return payment_controller(db).delete_payment(db, payment_id)
