from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.src.auth.controller import AuthController
from app.src.auth.dependencies import get_current_active_user, get_current_superuser
from app.src.auth.models import User
from app.src.auth.schemas import (
    LoginRequest,
    PasswordChange,
    Token,
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar novo usuário no sistema

    - **email**: Email único do usuário
    - **username**: Nome de usuário único
    - **password**: Senha (mínimo 6 caracteres, com letras e números)
    - **full_name**: Nome completo (opcional)
    """
    controller = AuthController(db)
    return controller.register(user_in)


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Realizar login e obter token de acesso

    - **username**: Email ou username do usuário
    - **password**: Senha do usuário

    Retorna um token JWT que deve ser usado no header Authorization: Bearer {token}
    """
    controller = AuthController(db)
    return controller.login(login_data)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Obter informações do usuário autenticado atual

    Requer autenticação via token JWT
    """
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Atualizar informações do usuário autenticado

    - **email**: Novo email (opcional)
    - **username**: Novo username (opcional)
    - **full_name**: Novo nome completo (opcional)

    Requer autenticação via token JWT
    """
    controller = AuthController(db)
    return controller.update_me(current_user, user_update)


@router.post("/change-password")
def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Alterar senha do usuário autenticado

    - **current_password**: Senha atual
    - **new_password**: Nova senha (mínimo 6 caracteres, com letras e números)

    Requer autenticação via token JWT
    """
    controller = AuthController(db)
    return controller.change_password(current_user, password_change)


# Rotas administrativas (apenas para superusuários)


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Listar todos os usuários do sistema

    Requer privilégios de superusuário
    """
    controller = AuthController(db)
    return controller.get_all_users(skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Obter usuário por ID

    Requer privilégios de superusuário
    """
    controller = AuthController(db)
    return controller.get_user_by_id(user_id)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """
    Deletar usuário do sistema

    Requer privilégios de superusuário
    """
    controller = AuthController(db)
    return controller.delete_user(user_id)
