from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from .schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from .controller import expense_controller

router = APIRouter()

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """Criar nova despesa"""
    return expense_controller(db).create_expense(db, expense)

@router.get("/", response_model=List[ExpenseResponse])
async def list_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar despesas"""
    return expense_controller(db).get_expenses(db, skip=skip, limit=limit)

@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Obter despesa por ID"""
    return expense_controller(db).get_expense_by_id(db, expense_id)

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar despesa"""
    return expense_controller(db).update_expense(db, expense_id, expense_update)

@router.delete("/{expense_id}")
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Deletar despesa"""
    return expense_controller(db).delete_expense(db, expense_id)
