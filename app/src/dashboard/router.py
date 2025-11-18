from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_current_user_id_from_token
from app.db.session import get_db
from app.src.contracts.models import Contract
from app.src.contracts.repository import ContractRepository
from app.src.expenses.repository import ExpenseRepository
from app.src.notifications.repository import NotificationRepository
from app.src.payments.models import Payment
from app.src.payments.repository import PaymentRepository
from app.src.properties.models import Property
from app.src.properties.repository import PropertyRepository
from app.src.tenants.models import Tenant
from app.src.tenants.repository import TenantRepository

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_from_token)
):
    """Obter estatísticas básicas do dashboard (filtrado por usuário)"""

    property_repo = PropertyRepository(db)
    tenant_repo = TenantRepository(db)
    contract_repo = ContractRepository(db)

    # Contar propriedades do usuário
    total_properties = db.query(func.count(Property.id)).filter(Property.user_id == user_id).scalar() or 0
    
    # Contar inquilinos do usuário
    total_tenants = db.query(func.count(Tenant.id)).filter(Tenant.user_id == user_id).scalar() or 0
    
    # Contar contratos ativos do usuário
    total_contracts = db.query(func.count(Contract.id)).filter(
        Contract.user_id == user_id,
        Contract.status == "active"
    ).scalar() or 0
    
    # Receita mensal (soma dos aluguéis de contratos ativos)
    monthly_revenue = db.query(func.sum(Contract.rent)).filter(
        Contract.user_id == user_id,
        Contract.status == "active"
    ).scalar() or 0.0

    return {
        "total_properties": total_properties,
        "total_tenants": total_tenants,
        "total_contracts": total_contracts,
        "monthly_revenue": float(monthly_revenue),
    }


@router.get("/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_from_token)
):
    """Obter resumo completo do dashboard (filtrado por usuário)"""

    property_repo = PropertyRepository(db)
    contract_repo = ContractRepository(db)
    payment_repo = PaymentRepository(db)

    # Contadores básicos
    total_properties = db.query(func.count(Property.id)).filter(Property.user_id == user_id).scalar() or 0
    
    active_contracts = db.query(func.count(Contract.id)).filter(
        Contract.user_id == user_id,
        Contract.status == "active"
    ).scalar() or 0
    
    # Contratos vencendo em 30 dias
    expiring_date = date.today() + timedelta(days=30)
    expiring_soon = db.query(func.count(Contract.id)).filter(
        Contract.user_id == user_id,
        Contract.status == "active",
        Contract.end_date <= expiring_date,
        Contract.end_date >= date.today()
    ).scalar() or 0

    # Receita mensal esperada (soma dos aluguéis ativos)
    monthly_revenue = db.query(func.sum(Contract.rent)).filter(
        Contract.user_id == user_id,
        Contract.status == "active"
    ).scalar() or 0.0

    # Pagamentos em atraso
    overdue_payments = len(payment_repo.get_overdue_payments(db, user_id))
    
    # Pagamentos pendentes
    pending_payments = len(payment_repo.get_pending_payments(db, user_id))

    return {
        "properties": {
            "total": total_properties,
            "active_contracts": active_contracts
        },
        "contracts": {
            "active": active_contracts,
            "expiring_soon": expiring_soon
        },
        "financial": {
            "monthly_revenue": float(monthly_revenue),
            "overdue_payments": overdue_payments,
            "pending_payments": pending_payments
        }
    }


@router.get("/revenue-chart")
async def get_revenue_chart(
    months: int = Query(default=12, ge=1, le=24),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_from_token)
):
    """Obter dados para gráfico de receitas (filtrado por usuário)"""
    chart_data = []
    current_date = date.today()

    for i in range(months):
        target_date = current_date - timedelta(days=30 * i)
        month = target_date.month
        year = target_date.year
        
        # Primeiro e último dia do mês
        from calendar import monthrange
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])

        # Somar pagamentos recebidos no mês
        revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.user_id == user_id,
            Payment.status == "paid",
            Payment.payment_date >= first_day,
            Payment.payment_date <= last_day
        ).scalar() or 0.0

        chart_data.append({
            "month": f"{year}-{month:02d}",
            "revenue": float(revenue)
        })

    return {"data": list(reversed(chart_data))}





@router.get("/property-performance")
async def get_property_performance(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_from_token)
):
    """Obter performance das propriedades do usuário"""
    property_repo = PropertyRepository(db)
    
    # Buscar todas as propriedades do usuário
    properties = property_repo.get_by_user(db, user_id, skip=0, limit=1000)
    performance_data = []

    current_month = date.today().month
    current_year = date.today().year
    
    # Primeiro e último dia do mês
    from calendar import monthrange
    first_day = date(current_year, current_month, 1)
    last_day = date(current_year, current_month, monthrange(current_year, current_month)[1])

    for prop in properties:
        # Contar contratos ativos para esta propriedade
        active_contracts = db.query(func.count(Contract.id)).filter(
            Contract.user_id == user_id,
            Contract.property_id == prop.id,
            Contract.status == "active"
        ).scalar() or 0
        
        # Receita da propriedade no mês (pagamentos recebidos)
        revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.user_id == user_id,
            Payment.property_id == prop.id,
            Payment.status == "paid",
            Payment.payment_date >= first_day,
            Payment.payment_date <= last_day
        ).scalar() or 0.0
        
        # Receita esperada (soma dos aluguéis dos contratos ativos)
        expected_revenue = db.query(func.sum(Contract.rent)).filter(
            Contract.user_id == user_id,
            Contract.property_id == prop.id,
            Contract.status == "active"
        ).scalar() or 0.0

        performance_data.append(
            {
                "property_id": prop.id,
                "property_name": prop.name,
                "property_address": prop.address,
                "active_contracts": active_contracts,
                "revenue_received": float(revenue),
                "revenue_expected": float(expected_revenue),
                "collection_rate": round((revenue / expected_revenue * 100) if expected_revenue > 0 else 0, 2)
            }
        )

    return {"properties": performance_data}


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_from_token)
):
    """Obter atividades recentes do usuário"""
    
    # Pagamentos recentes (últimos 5)
    recent_payments = db.query(Payment).filter(
        Payment.user_id == user_id
    ).order_by(Payment.created_at.desc()).limit(limit // 2).all()

    # Contratos recentes (últimos 5)
    recent_contracts = db.query(Contract).filter(
        Contract.user_id == user_id
    ).order_by(Contract.created_at.desc()).limit(limit // 2).all()

    activities = []

    # Adicionar pagamentos
    for payment in recent_payments:
        activities.append(
            {
                "type": "payment",
                "description": f"Pagamento de R$ {payment.amount:.2f} - Status: {payment.status}",
                "date": str(payment.payment_date or payment.due_date),
                "related_id": payment.id,
                "created_at": str(payment.created_at) if hasattr(payment, 'created_at') else str(payment.due_date)
            }
        )

    # Adicionar contratos
    for contract in recent_contracts:
        activities.append(
            {
                "type": "contract",
                "description": f"Contrato criado - Status: {contract.status}",
                "date": str(contract.start_date),
                "related_id": contract.id,
                "created_at": str(contract.created_at) if hasattr(contract, 'created_at') else str(contract.start_date)
            }
        )

    # Ordenar por created_at se disponível, senão por date
    activities.sort(key=lambda x: x.get("created_at", x["date"]), reverse=True)

    return {"activities": activities[:limit]}
