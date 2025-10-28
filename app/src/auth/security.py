from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configuração do contexto de criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar se a senha em texto plano corresponde ao hash

    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash da senha armazenada

    Returns:
        bool: True se as senhas correspondem, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Criar hash da senha

    Args:
        password: Senha em texto plano

    Returns:
        str: Senha hasheada
    """
    return pwd_context.hash(password)  # type: ignore[no-any-return]


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Criar token JWT de acesso

    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração do token

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodificar token JWT

    Args:
        token: Token JWT para decodificar

    Returns:
        dict: Dados decodificados do token ou None se inválido
    """
    try:
        payload: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
