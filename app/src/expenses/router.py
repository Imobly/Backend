from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from .repository import get_expense_repository
from .schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Criar nova despesa"""
    expense_repo = get_expense_repository(db)
    return expense_repo.create(db, obj_in=expense)


@router.get("/", response_model=List[ExpenseResponse])
async def list_expenses(
    skip: int = 0,
    limit: int = 100,
    property_id: int = None,
    category: str = None,
    month: int = None,
    year: int = None,
    db: Session = Depends(get_db),
):
    """Listar despesas"""
    expense_repo = get_expense_repository(db)
    expenses = expense_repo.get_multi(db, skip=skip, limit=limit)

    # Aplicar filtros
    if property_id:
        expenses = [e for e in expenses if e.property_id == property_id]
    if category:
        expenses = [e for e in expenses if e.category == category]

    # Filtrar por mês/ano se especificado
    if month or year:
        filtered_expenses = []
        for expense in expenses:
            expense_date = expense.date
            if month and expense_date.month != month:
                continue
            if year and expense_date.year != year:
                continue
            filtered_expenses.append(expense)
        expenses = filtered_expenses

    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Obter despesa por ID"""
    expense_repo = get_expense_repository(db)
    expense = expense_repo.get(db, expense_id)

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Despesa não encontrada")

    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)
):
    """Atualizar despesa"""
    expense_repo = get_expense_repository(db)
    expense = expense_repo.get(db, expense_id)

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Despesa não encontrada")

    updated_expense = expense_repo.update(db, db_obj=expense, obj_in=expense_update)
    return updated_expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Deletar despesa"""
    expense_repo = get_expense_repository(db)
    expense = expense_repo.get(db, expense_id)

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Despesa não encontrada")

    expense_repo.delete(db, id=expense_id)


@router.get("/property/{property_id}/monthly", response_model=dict)
async def get_monthly_expenses(
    property_id: int, year: int, month: int, db: Session = Depends(get_db)
):
    """Obter despesas mensais de uma propriedade"""
    expense_repo = get_expense_repository(db)
    expenses = expense_repo.get_by_property(db, property_id)

    # Filtrar por mês/ano
    monthly_expenses = []
    for expense in expenses:
        if expense.date.year == year and expense.date.month == month:
            monthly_expenses.append(expense)

    total = sum(expense.amount for expense in monthly_expenses)

    return {
        "property_id": property_id,
        "year": year,
        "month": month,
        "total_expenses": total,
        "count": len(monthly_expenses),
        "expenses": monthly_expenses,
    }


@router.get("/categories/summary", response_model=dict)
async def get_expenses_by_category(
    property_id: int = None, year: int = None, month: int = None, db: Session = Depends(get_db)
):
    """Obter resumo de despesas por categoria"""
    expense_repo = get_expense_repository(db)
    expenses = expense_repo.get_multi(db)

    # Aplicar filtros
    if property_id:
        expenses = [e for e in expenses if e.property_id == property_id]
    if year:
        expenses = [e for e in expenses if e.date.year == year]
    if month:
        expenses = [e for e in expenses if e.date.month == month]

    # Agrupar por categoria
    categories = {}
    for expense in expenses:
        if expense.category not in categories:
            categories[expense.category] = {"total": 0, "count": 0, "expenses": []}
        categories[expense.category]["total"] += expense.amount
        categories[expense.category]["count"] += 1
        categories[expense.category]["expenses"].append(expense)

    return {"categories": categories}
