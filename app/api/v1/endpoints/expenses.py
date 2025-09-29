from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, Expense
from app.expenses.repository import expense_repository

router = APIRouter()

@router.post("/", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """Criar nova despesa"""
    expense_repo = expense_repository(db)
    
    # Verificar se propriedade existe
    if not expense_repo.property_exists(expense.property_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propriedade não encontrada"
        )
    
    db_expense = expense_repo.create(expense)
    return db_expense

@router.get("/", response_model=List[Expense])
async def list_expenses(
    skip: int = 0,
    limit: int = 100,
    property_id: int = None,
    category: str = None,
    month: int = None,
    year: int = None,
    db: Session = Depends(get_db)
):
    """Listar despesas"""
    expense_repo = expense_repository(db)
    
    filters = {}
    if property_id:
        filters["property_id"] = property_id
    if category:
        filters["category"] = category
    
    expenses = expense_repo.get_multi(skip=skip, limit=limit, **filters)
    
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

@router.get("/{expense_id}", response_model=Expense)
async def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Obter despesa por ID"""
    expense_repo = expense_repository(db)
    expense = expense_repo.get(expense_id)
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Despesa não encontrada"
        )
    
    return expense

@router.put("/{expense_id}", response_model=Expense)
async def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar despesa"""
    expense_repo = expense_repository(db)
    expense = expense_repo.get(expense_id)
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Despesa não encontrada"
        )
    
    updated_expense = expense_repo.update(expense_id, expense_update)
    return updated_expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Deletar despesa"""
    expense_repo = expense_repository(db)
    expense = expense_repo.get(expense_id)
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Despesa não encontrada"
        )
    
    expense_repo.delete(expense_id)

@router.get("/property/{property_id}/monthly", response_model=dict)
async def get_monthly_expenses(
    property_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """Obter despesas mensais de uma propriedade"""
    expense_repo = expense_repository(db)
    
    # Verificar se propriedade existe
    if not expense_repo.property_exists(property_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propriedade não encontrada"
        )
    
    expenses_summary = expense_repo.get_monthly_expenses(property_id, year, month)
    return expenses_summary

@router.get("/categories/summary", response_model=dict)
async def get_expenses_by_category(
    property_id: int = None,
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db)
):
    """Obter resumo de despesas por categoria"""
    expense_repo = expense_repository(db)
    summary = expense_repo.get_expenses_by_category(property_id, year, month)
    return summary