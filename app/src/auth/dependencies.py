from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.src.auth.models import User
from app.src.auth.repository import UserRepository
from app.src.auth.security import decode_access_token

# Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Obter usuário atual a partir do token JWT

    Args:
        credentials: Credenciais HTTP Bearer
        db: Sessão do banco de dados

    Returns:
        User: Usuário autenticado

    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user_repo = UserRepository()
    user = user_repo.get(db, int(user_id))

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Obter usuário ativo atual

    Args:
        current_user: Usuário atual da dependência get_current_user

    Returns:
        User: Usuário ativo autenticado

    Raises:
        HTTPException: Se o usuário estiver inativo
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Obter superusuário atual

    Args:
        current_user: Usuário atual da dependência get_current_user

    Returns:
        User: Superusuário autenticado

    Raises:
        HTTPException: Se o usuário não for superusuário
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não possui privilégios suficientes",
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Obter usuário atual opcional (não levanta exceção se não autenticado)

    Args:
        credentials: Credenciais HTTP Bearer (opcional)
        db: Sessão do banco de dados

    Returns:
        User ou None: Usuário autenticado ou None se não autenticado
    """
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        return None

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        return None

    user_repo = UserRepository()
    user = user_repo.get(db, int(user_id))

    if user is None or not user.is_active:
        return None

    return user
