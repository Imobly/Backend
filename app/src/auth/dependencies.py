from typing import Optional, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.src.auth.security import decode_access_token

# Bearer token security scheme
security = HTTPBearer()


async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict:
    """
    Validar token JWT e extrair informações do usuário
    
    O Backend não gerencia usuários, apenas valida tokens do Auth-api.
    Retorna os dados do payload do token JWT.

    Args:
        credentials: Credenciais HTTP Bearer

    Returns:
        Dict: Payload do token contendo user_id, username, etc.

    Raises:
        HTTPException: Se o token for inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    username: Optional[str] = payload.get("username")
    
    if user_id is None:
        raise credentials_exception

    # Retorna informações do usuário do token (não do banco)
    return {
        "user_id": int(user_id),
        "username": username,
        "token_payload": payload
    }


# Mantém compatibilidade com código legado que espera User object
# DEPRECATED: Use get_current_user_token para novos endpoints
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    DEPRECATED: Backend não deve ter tabela users.
    Use get_current_user_token para validação stateless.
    
    Esta função existe apenas para compatibilidade com código legado.
    """
    user_data = await get_current_user_token(credentials)
    
    # Cria um objeto simples com os dados do token
    class TokenUser:
        def __init__(self, user_id: int, username: str):
            self.id = user_id
            self.username = username
            self.is_active = True  # Assume ativo se token é válido
    
    return TokenUser(user_data["user_id"], user_data["username"])


async def get_current_active_user(
    current_user = Depends(get_current_user),
):
    """
    Obter usuário ativo atual (compatibilidade)
    
    Como tokens do Auth-api são sempre de usuários ativos,
    apenas retorna o usuário.
    """
    return current_user


async def get_current_superuser(
    current_user = Depends(get_current_user),
):
    """
    DEPRECATED: Backend não gerencia permissões de usuário.
    Permissões devem ser gerenciadas pelo Auth-api.
    
    Por ora, aceita qualquer usuário autenticado.
    """
    # TODO: Implementar verificação de permissões via Auth-api
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
):
    """
    Obter dados do usuário opcional (não levanta exceção se não autenticado)

    Args:
        credentials: Credenciais HTTP Bearer (opcional)

    Returns:
        Dict ou None: Dados do usuário ou None se não autenticado
    """
    if credentials is None:
        return None
        
    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        
        if payload is None:
            return None
            
        user_id = payload.get("sub")
        username = payload.get("username")
        
        if user_id is None:
            return None
            
        class TokenUser:
            def __init__(self, user_id: int, username: str):
                self.id = user_id
                self.username = username
                self.is_active = True
        
        return TokenUser(int(user_id), username)
    except Exception:
        return None
