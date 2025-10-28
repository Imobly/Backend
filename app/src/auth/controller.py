from datetime import timedelta
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.src.auth.models import User
from app.src.auth.repository import UserRepository
from app.src.auth.schemas import (
    LoginRequest,
    PasswordChange,
    Token,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.src.auth.security import create_access_token, verify_password


class AuthController:
    """Controller para operações de autenticação"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()

    def register(self, user_in: UserCreate) -> UserResponse:
        """
        Registrar novo usuário

        Args:
            user_in: Dados do novo usuário

        Returns:
            UserResponse: Usuário criado

        Raises:
            HTTPException: Se email ou username já existirem
        """
        # Verificar se email ou username já existem
        constraints = self.repository.check_unique_constraints(
            self.db, user_in.email, user_in.username
        )

        if constraints["email_exists"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado no sistema",
            )

        if constraints["username_exists"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso",
            )

        # Criar usuário
        user = self.repository.create_user(self.db, user_in)
        return UserResponse.model_validate(user)

    def login(self, login_data: LoginRequest) -> Token:
        """
        Realizar login de usuário

        Args:
            login_data: Credenciais de login

        Returns:
            Token: Token de acesso JWT

        Raises:
            HTTPException: Se as credenciais forem inválidas
        """
        # Buscar usuário por email ou username
        user = self.repository.get_by_email_or_username(self.db, login_data.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verificar senha
        if not verify_password(login_data.password, str(user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verificar se usuário está ativo
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )

        # Criar token de acesso
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires,
        )

        return Token(access_token=access_token, token_type="bearer")

    def get_me(self, current_user: User) -> UserResponse:
        """
        Obter informações do usuário atual

        Args:
            current_user: Usuário autenticado

        Returns:
            UserResponse: Dados do usuário
        """
        return UserResponse.model_validate(current_user)

    def update_me(self, current_user: User, user_update: UserUpdate) -> UserResponse:
        """
        Atualizar informações do usuário atual

        Args:
            current_user: Usuário autenticado
            user_update: Dados a atualizar

        Returns:
            UserResponse: Usuário atualizado

        Raises:
            HTTPException: Se email ou username já existirem
        """
        # Verificar unicidade se email ou username forem atualizados
        if user_update.email and user_update.email != current_user.email:
            existing_user = self.repository.get_by_email(self.db, user_update.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado no sistema",
                )

        if user_update.username and user_update.username != current_user.username:
            existing_user = self.repository.get_by_username(self.db, user_update.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username já está em uso",
                )

        # Atualizar usuário
        updated_user = self.repository.update(self.db, int(current_user.id), user_update)
        return UserResponse.model_validate(updated_user)

    def change_password(self, current_user: User, password_change: PasswordChange) -> dict:
        """
        Alterar senha do usuário

        Args:
            current_user: Usuário autenticado
            password_change: Dados da alteração de senha

        Returns:
            dict: Mensagem de sucesso

        Raises:
            HTTPException: Se a senha atual for incorreta
        """
        # Verificar senha atual
        if not verify_password(password_change.current_password, str(current_user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta",
            )

        # Atualizar senha
        self.repository.update_password(self.db, current_user, password_change.new_password)

        return {"message": "Senha alterada com sucesso"}

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """
        Listar todos os usuários (apenas para superusuários)

        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar

        Returns:
            List[UserResponse]: Lista de usuários
        """
        users = self.repository.get_multi(self.db, skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Obter usuário por ID (apenas para superusuários)

        Args:
            user_id: ID do usuário

        Returns:
            UserResponse: Dados do usuário

        Raises:
            HTTPException: Se o usuário não for encontrado
        """
        user = self.repository.get(self.db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return UserResponse.model_validate(user)

    def delete_user(self, user_id: int) -> dict:
        """
        Deletar usuário (apenas para superusuários)

        Args:
            user_id: ID do usuário a deletar

        Returns:
            dict: Mensagem de sucesso

        Raises:
            HTTPException: Se o usuário não for encontrado
        """
        user = self.repository.get(self.db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        self.repository.remove(self.db, user_id)
        return {"message": "Usuário deletado com sucesso"}
