from typing import List, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.src.auth.security import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware de autenticação para validar tokens JWT

    Este middleware verifica se o token JWT é válido em todas as requisições
    (exceto rotas públicas definidas em PUBLIC_ROUTES)
    """

    # Rotas que não requerem autenticação
    PUBLIC_ROUTES = [
        "/",
        "/health",
        "/api/v1/docs",
        "/api/v1/openapi.json",
        "/api/v1/redoc",
        "/api/v1/auth/register",
        "/api/v1/auth/login",
    ]

    async def dispatch(self, request: Request, call_next):
        """
        Processar requisição e validar token

        Args:
            request: Requisição HTTP
            call_next: Próximo handler na cadeia

        Returns:
            Response: Resposta HTTP
        """
        # Verificar se a rota é pública
        path = request.url.path
        if self._is_public_route(path):
            response = await call_next(request)
            return response

        # Obter token do header Authorization
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token de autenticação é necessário"},
            )

        # Validar formato do header
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Esquema de autenticação inválido. Use 'Bearer'"},
                )
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Formato do header Authorization inválido"},
            )

        # Validar token
        payload = decode_access_token(token)
        if payload is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido ou expirado"},
            )

        # Adicionar dados do usuário ao request state
        request.state.user_id = payload.get("sub")
        request.state.username = payload.get("username")

        # Continuar processamento
        response = await call_next(request)
        return response

    def _is_public_route(self, path: str) -> bool:
        """
        Verificar se a rota é pública

        Args:
            path: Caminho da URL

        Returns:
            bool: True se a rota for pública
        """
        # Verificar rotas exatas
        if path in self.PUBLIC_ROUTES:
            return True

        # Verificar prefixos de rotas públicas
        public_prefixes = [
            "/uploads/",
            "/static/",
        ]
        for prefix in public_prefixes:
            if path.startswith(prefix):
                return True

        return False


def create_auth_middleware(
    public_routes: Optional[List[str]] = None,
) -> type[AuthMiddleware]:
    """
    Factory para criar middleware de autenticação com rotas públicas customizadas

    Args:
        public_routes: Lista de rotas públicas adicionais

    Returns:
        type[AuthMiddleware]: Classe do middleware
    """
    if public_routes:
        AuthMiddleware.PUBLIC_ROUTES.extend(public_routes)

    return AuthMiddleware
