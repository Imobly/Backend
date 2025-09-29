from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

from app.db.session import get_db
from app.properties.repository import property_repository
from app.contracts.repository import contract_repository
from app.payments.repository import payment_repository
from app.expenses.repository import expense_repository
from app.notifications.repository import notification_repository

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Obter resumo do dashboard"""
    
    property_repo = property_repository(db)
    contract_repo = contract_repository(db)
    payment_repo = payment_repository(db)
    expense_repo = expense_repository(db)
    notification_repo = notification_repository(db)
    
    # Contadores básicos
    total_properties = property_repo.count_all()
    total_contracts = contract_repo.count_active()
    total_units = property_repo.count_total_units()
    occupied_units = contract_repo.count_occupied_units()
    
    # Taxa de ocupação
    occupancy_rate = (occupied_units / total_units * 100) if total_units > 0 else 0
    
    # Receitas e despesas do mês atual
    current_month = date.today().month
    current_year = date.today().year
    
    monthly_revenue = payment_repo.get_monthly_revenue(current_year, current_month)
    monthly_expenses = expense_repo.get_monthly_total(current_year, current_month)
    
    # Lucro líquido
    net_profit = monthly_revenue - monthly_expenses
    
    # Pagamentos em atraso
    overdue_payments = len(payment_repo.get_overdue_payments())
    
    # Contratos vencendo em 30 dias
    expiring_contracts = len(contract_repo.get_expiring_contracts(30))
    
    # Notificações não lidas
    unread_notifications = notification_repo.get_unread_count()
    
    return {
        "properties": {
            "total": total_properties,
            "total_units": total_units,
            "occupied_units": occupied_units,
            "occupancy_rate": round(occupancy_rate, 2)
        },
        "contracts": {
            "active": total_contracts,
            "expiring_soon": expiring_contracts
        },
        "financial": {
            "monthly_revenue": monthly_revenue,
            "monthly_expenses": monthly_expenses,
            "net_profit": net_profit,
            "overdue_payments": overdue_payments
        },
        "notifications": {
            "unread_count": unread_notifications
        }
    }

@router.get("/revenue-chart")
async def get_revenue_chart(
    months: int = 12,
    db: Session = Depends(get_db)
):
    """Obter dados para gráfico de receitas"""
    payment_repo = payment_repository(db)
    
    chart_data = []
    current_date = date.today()
    
    for i in range(months):
        target_date = current_date - timedelta(days=30 * i)
        month = target_date.month
        year = target_date.year
        
        revenue = payment_repo.get_monthly_revenue(year, month)
        
        chart_data.append({
            "month": f"{year}-{month:02d}",
            "revenue": revenue
        })
    
    return {"data": list(reversed(chart_data))}

@router.get("/expense-chart")
async def get_expense_chart(
    months: int = 12,
    db: Session = Depends(get_db)
):
    """Obter dados para gráfico de despesas"""
    expense_repo = expense_repository(db)
    
    chart_data = []
    current_date = date.today()
    
    for i in range(months):
        target_date = current_date - timedelta(days=30 * i)
        month = target_date.month
        year = target_date.year
        
        expenses = expense_repo.get_monthly_total(year, month)
        
        chart_data.append({
            "month": f"{year}-{month:02d}",
            "expenses": expenses
        })
    
    return {"data": list(reversed(chart_data))}

@router.get("/property-performance")
async def get_property_performance(db: Session = Depends(get_db)):
    """Obter performance das propriedades"""
    property_repo = property_repository(db)
    payment_repo = payment_repository(db)
    expense_repo = expense_repository(db)
    
    properties = property_repo.get_all()
    performance_data = []
    
    current_month = date.today().month
    current_year = date.today().year
    
    for prop in properties:
        revenue = payment_repo.get_property_monthly_revenue(prop.id, current_year, current_month)
        expenses = expense_repo.get_property_monthly_total(prop.id, current_year, current_month)
        net_income = revenue - expenses
        
        occupied_units = property_repo.get_occupied_units_count(prop.id)
        total_units = property_repo.get_total_units_count(prop.id)
        occupancy_rate = (occupied_units / total_units * 100) if total_units > 0 else 0
        
        performance_data.append({
            "property_id": prop.id,
            "property_name": prop.name,
            "revenue": revenue,
            "expenses": expenses,
            "net_income": net_income,
            "occupancy_rate": round(occupancy_rate, 2),
            "occupied_units": occupied_units,
            "total_units": total_units
        })
    
    return {"properties": performance_data}

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Obter atividades recentes"""
    payment_repo = payment_repository(db)
    contract_repo = contract_repository(db)
    
    # Pagamentos recentes
    recent_payments = payment_repo.get_recent_payments(limit // 2)
    
    # Contratos recentes
    recent_contracts = contract_repo.get_recent_contracts(limit // 2)
    
    activities = []
    
    # Adicionar pagamentos
    for payment in recent_payments:
        activities.append({
            "type": "payment",
            "description": f"Pagamento de R$ {payment.amount:.2f} confirmado",
            "date": payment.payment_date or payment.due_date,
            "related_id": payment.id
        })
    
    # Adicionar contratos
    for contract in recent_contracts:
        activities.append({
            "type": "contract",
            "description": f"Novo contrato criado - {contract.unit.property.name}",
            "date": contract.start_date,
            "related_id": contract.id
        })
    
    # Ordenar por data
    activities.sort(key=lambda x: x["date"], reverse=True)
    
    return {"activities": activities[:limit]}