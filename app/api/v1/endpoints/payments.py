from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.schemas.payment import PaymentCreate, PaymentUpdate, Payment
from app.payments.repository import payment_repository

router = APIRouter()

@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Criar novo pagamento"""
    payment_repo = payment_repository(db)
    
    # Verificar se contrato existe
    if not payment_repo.contract_exists(payment.contract_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    db_payment = payment_repo.create(payment)
    return db_payment

@router.get("/", response_model=List[Payment])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    contract_id: int = None,
    status: str = None,
    month: int = None,
    year: int = None,
    db: Session = Depends(get_db)
):
    """Listar pagamentos"""
    payment_repo = payment_repository(db)
    
    filters = {}
    if contract_id:
        filters["contract_id"] = contract_id
    if status:
        filters["status"] = status
    
    payments = payment_repo.get_multi(skip=skip, limit=limit, **filters)
    
    # Filtrar por mês/ano se especificado
    if month or year:
        filtered_payments = []
        for payment in payments:
            payment_date = payment.due_date
            if month and payment_date.month != month:
                continue
            if year and payment_date.year != year:
                continue
            filtered_payments.append(payment)
        payments = filtered_payments
    
    return payments

@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Obter pagamento por ID"""
    payment_repo = payment_repository(db)
    payment = payment_repo.get(payment_id)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado"
        )
    
    return payment

@router.put("/{payment_id}", response_model=Payment)
async def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar pagamento"""
    payment_repo = payment_repository(db)
    payment = payment_repo.get(payment_id)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado"
        )
    
    updated_payment = payment_repo.update(payment_id, payment_update)
    return updated_payment

@router.post("/{payment_id}/confirm", response_model=Payment)
async def confirm_payment(
    payment_id: int,
    payment_date: date = None,
    amount_paid: float = None,
    db: Session = Depends(get_db)
):
    """Confirmar pagamento"""
    payment_repo = payment_repository(db)
    payment = payment_repo.get(payment_id)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado"
        )
    
    if payment.status == "pago":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pagamento já foi confirmado"
        )
    
    confirmed_payment = payment_repo.confirm_payment(
        payment_id, 
        payment_date or date.today(), 
        amount_paid
    )
    return confirmed_payment

@router.get("/overdue/list", response_model=List[Payment])
async def get_overdue_payments(db: Session = Depends(get_db)):
    """Obter pagamentos em atraso"""
    payment_repo = payment_repository(db)
    payments = payment_repo.get_overdue_payments()
    return payments

@router.get("/contract/{contract_id}/generate/{year}", response_model=List[Payment])
async def generate_annual_payments(
    contract_id: int,
    year: int,
    db: Session = Depends(get_db)
):
    """Gerar pagamentos anuais para um contrato"""
    payment_repo = payment_repository(db)
    
    # Verificar se contrato existe
    if not payment_repo.contract_exists(contract_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    payments = payment_repo.generate_annual_payments(contract_id, year)
    return payments

@router.post("/bulk-confirm", response_model=List[Payment])
async def bulk_confirm_payments(
    payment_ids: List[int],
    payment_date: date = None,
    db: Session = Depends(get_db)
):
    """Confirmar múltiplos pagamentos"""
    payment_repo = payment_repository(db)
    
    confirmed_payments = []
    for payment_id in payment_ids:
        payment = payment_repo.get(payment_id)
        if payment and payment.status != "pago":
            confirmed_payment = payment_repo.confirm_payment(
                payment_id, 
                payment_date or date.today()
            )
            confirmed_payments.append(confirmed_payment)
    
    return confirmed_payments