from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id_from_token
from app.core.payment_service import PaymentCalculationService
from app.core.notification_service import NotificationService
from app.db.session import get_db
from app.src.contracts.models import Contract

from .controller import payment_controller
from .models import Payment
from .schemas import (
    PaymentCalculateRequest,
    PaymentCalculateResponse,
    PaymentCreate,
    PaymentRegisterRequest,
    PaymentResponse,
    PaymentUpdate
)

router = APIRouter()


@router.post("/calculate", response_model=PaymentCalculateResponse)
async def calculate_payment_values(
    request: PaymentCalculateRequest,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """
    Calcula automaticamente valores de pagamento com multa e juros
    
    Este endpoint calcula:
    - Multa (aplicada uma vez)
    - Juros (proporcional aos dias de atraso)
    - Valor total esperado
    - Status do pagamento
    - Valor restante (se pagamento parcial)
    """
    # Buscar contrato
    contract = db.query(Contract).filter(
        Contract.id == request.contract_id,
        Contract.user_id == user_id
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    # Calcular valores
    calculation = PaymentCalculationService.calculate_payment_values(
        contract=contract,
        due_date=request.due_date,
        payment_date=request.payment_date,
        paid_amount=request.paid_amount
    )
    
    return PaymentCalculateResponse(**calculation)


@router.post("/register", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def register_payment(
    request: PaymentRegisterRequest,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """
    Registra pagamento com cálculo automático de multa e juros
    
    Este endpoint:
    - Calcula automaticamente multa e juros baseado no contrato
    - Determina o status automaticamente
    - Cria notificação de pagamento recebido
    """
    # Buscar contrato
    contract = db.query(Contract).filter(
        Contract.id == request.contract_id,
        Contract.user_id == user_id
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    # Calcular valores automaticamente
    calculation = PaymentCalculationService.calculate_payment_values(
        contract=contract,
        due_date=request.due_date,
        payment_date=request.payment_date,
        paid_amount=request.paid_amount
    )
    
    # Criar pagamento com valores calculados
    payment_data = PaymentCreate(
        property_id=contract.property_id,
        tenant_id=contract.tenant_id,
        contract_id=contract.id,
        due_date=request.due_date,
        payment_date=request.payment_date,
        amount=request.paid_amount,
        fine_amount=calculation["fine_amount"] + calculation["interest_amount"],
        total_amount=calculation["total_expected"],
        status=calculation["status"],
        payment_method=request.payment_method,
        description=request.description
    )
    
    payment = payment_controller(db).create_payment(db, user_id, payment_data)
    
    # Criar notificação de pagamento recebido
    NotificationService.create_payment_received_notification(db, payment)
    
    return payment


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Criar novo pagamento"""
    return payment_controller(db).create_payment(db, user_id, payment)


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Listar pagamentos"""
    return payment_controller(db).get_payments(db, user_id, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Obter pagamento por ID"""
    return payment_controller(db).get_payment_by_id(db, payment_id, user_id)


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Atualizar pagamento"""
    return payment_controller(db).update_payment(db, payment_id, user_id, payment_update)


@router.delete("/{payment_id}")
async def delete_payment(
    payment_id: int,
    user_id: int = Depends(get_current_user_id_from_token),
    db: Session = Depends(get_db)
):
    """Deletar pagamento"""
    return payment_controller(db).delete_payment(db, payment_id, user_id)
