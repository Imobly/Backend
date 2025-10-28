from typing import Optional

from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.src.auth.models import User
from app.src.auth.schemas import UserCreate, UserUpdate
from app.src.auth.security import get_password_hash


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repositório para operações de usuário"""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Buscar usuário por email

        Args:
            db: Sessão do banco de dados
            email: Email do usuário

        Returns:
            User ou None se não encontrado
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Buscar usuário por username

        Args:
            db: Sessão do banco de dados
            username: Username do usuário

        Returns:
            User ou None se não encontrado
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_email_or_username(self, db: Session, identifier: str) -> Optional[User]:
        """
        Buscar usuário por email ou username

        Args:
            db: Sessão do banco de dados
            identifier: Email ou username do usuário

        Returns:
            User ou None se não encontrado
        """
        return (
            db.query(User)
            .filter((User.email == identifier) | (User.username == identifier))
            .first()
        )

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Criar novo usuário

        Args:
            db: Sessão do banco de dados
            user_in: Dados do usuário a criar

        Returns:
            User: Usuário criado
        """
        user_data = user_in.model_dump(exclude={"password"})
        user_data["hashed_password"] = get_password_hash(user_in.password)

        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def update_password(self, db: Session, user: User, new_password: str) -> User:
        """
        Atualizar senha do usuário

        Args:
            db: Sessão do banco de dados
            user: Usuário a atualizar
            new_password: Nova senha em texto plano

        Returns:
            User: Usuário atualizado
        """
        hashed_password: str = get_password_hash(new_password)
        user.hashed_password = hashed_password  # type: ignore[assignment]
        db.commit()
        db.refresh(user)

        return user

    def check_unique_constraints(self, db: Session, email: str, username: str) -> dict:
        """
        Verificar se email e username já existem

        Args:
            db: Sessão do banco de dados
            email: Email a verificar
            username: Username a verificar

        Returns:
            dict: Dicionário com 'email_exists' e 'username_exists'
        """
        email_exists = self.get_by_email(db, email) is not None
        username_exists = self.get_by_username(db, username) is not None

        return {"email_exists": email_exists, "username_exists": username_exists}

    def update(self, db: Session, user_id: int, obj_in: UserUpdate) -> User:  # type: ignore[override]
        """
        Atualizar usuário

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            obj_in: Dados para atualizar

        Returns:
            User: Usuário atualizado
        """
        db_obj = self.get(db, user_id)
        if db_obj is None:
            raise ValueError(f"User with id {user_id} not found")
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, user_id: int) -> User:
        """
        Remover usuário

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário

        Returns:
            User: Usuário removido
        """
        return self.delete(db, id=user_id)
