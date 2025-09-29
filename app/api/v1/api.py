from fastapi import APIRouter

# Importar routers das novas features
from app.properties.router import router as properties_router
from app.tenants.router import router as tenants_router
from app.units.router import router as units_router
from app.contracts.router import router as contracts_router
from app.payments.router import router as payments_router
from app.expenses.router import router as expenses_router
from app.notifications.router import router as notifications_router
from app.dashboard.router import router as dashboard_router

api_router = APIRouter()

# Incluir todos os routers com seus prefixos e tags
api_router.include_router(
    properties_router, 
    prefix="/properties", 
    tags=["properties"]
)
api_router.include_router(
    tenants_router, 
    prefix="/tenants", 
    tags=["tenants"]
)
api_router.include_router(
    units_router, 
    prefix="/units", 
    tags=["units"]
)
api_router.include_router(
    contracts_router, 
    prefix="/contracts", 
    tags=["contracts"]
)
api_router.include_router(
    payments_router, 
    prefix="/payments", 
    tags=["payments"]
)
api_router.include_router(
    expenses_router, 
    prefix="/expenses", 
    tags=["expenses"]
)
api_router.include_router(
    notifications_router, 
    prefix="/notifications", 
    tags=["notifications"]
)
api_router.include_router(
    dashboard_router, 
    prefix="/dashboard", 
    tags=["dashboard"]
)