# Sistema de Autenticação - Imóvel Gestão API

## Visão Geral

O sistema de autenticação foi implementado utilizando JWT (JSON Web Tokens) e segue as melhores práticas de segurança.

## Arquitetura

### Estrutura de Arquivos

```
app/src/auth/
├── __init__.py
├── models.py          # Modelo User do SQLAlchemy
├── schemas.py         # Schemas Pydantic para validação
├── repository.py      # Repositório para operações de banco de dados
├── controller.py      # Lógica de negócios
├── router.py          # Endpoints da API
├── security.py        # Funções de criptografia e JWT
├── dependencies.py    # Dependências FastAPI (get_current_user, etc)
└── middleware.py      # Middleware de autenticação (opcional)
```

## Endpoints

### 1. Registro de Usuário

**POST** `/api/v1/auth/register`

Registrar novo usuário no sistema.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "username": "usuario123",
  "password": "senha123",
  "full_name": "Nome Completo" // opcional
}
```

**Validações:**
- Email válido e único
- Username único (3-100 caracteres)
- Senha mínimo 6 caracteres, com letras e números
- Full name opcional (máximo 255 caracteres)

**Response (201):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "username": "usuario123",
  "full_name": "Nome Completo",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-27T23:00:00"
}
```

### 2. Login

**POST** `/api/v1/auth/login`

Realizar login e obter token de acesso.

**Request Body:**
```json
{
  "username": "usuario123", // pode ser email ou username
  "password": "senha123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Uso do Token:**
Adicione o token no header de todas as requisições protegidas:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Obter Usuário Atual

**GET** `/api/v1/auth/me`

Obter informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "username": "usuario123",
  "full_name": "Nome Completo",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-27T23:00:00"
}
```

### 4. Atualizar Perfil

**PUT** `/api/v1/auth/me`

Atualizar informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body (todos os campos opcionais):**
```json
{
  "email": "novoemail@example.com",
  "username": "novousername",
  "full_name": "Novo Nome"
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "novoemail@example.com",
  "username": "novousername",
  "full_name": "Novo Nome",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-27T23:00:00"
}
```

### 5. Alterar Senha

**POST** `/api/v1/auth/change-password`

Alterar senha do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "current_password": "senhaatual123",
  "new_password": "novasenha456"
}
```

**Response (200):**
```json
{
  "message": "Senha alterada com sucesso"
}
```

### 6. Listar Usuários (Admin)

**GET** `/api/v1/auth/users?skip=0&limit=100`

Listar todos os usuários (apenas superusuários).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "email": "usuario@example.com",
    "username": "usuario123",
    "full_name": "Nome Completo",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2025-10-27T23:00:00"
  }
]
```

### 7. Obter Usuário por ID (Admin)

**GET** `/api/v1/auth/users/{user_id}`

Obter usuário específico por ID (apenas superusuários).

### 8. Deletar Usuário (Admin)

**DELETE** `/api/v1/auth/users/{user_id}`

Deletar usuário do sistema (apenas superusuários).

## Segurança

### Criptografia de Senha
- Utiliza bcrypt com salt automático
- Hash armazenado na coluna `hashed_password`
- Senha nunca é retornada nas respostas

### JWT Token
- Algoritmo: HS256
- Expiração: 30 minutos (configurável)
- Payload contém: `sub` (user_id), `username`, `exp`
- Secret key deve ser alterada em produção

### Middleware (Opcional)

O sistema inclui um middleware de autenticação que pode ser habilitado globalmente.

**Para habilitar no `app/main.py`:**
```python
from app.src.auth.middleware import AuthMiddleware

app.add_middleware(AuthMiddleware)
```

**Rotas públicas (não requerem token):**
- `/`
- `/health`
- `/api/v1/docs`
- `/api/v1/redoc`
- `/api/v1/openapi.json`
- `/api/v1/auth/register`
- `/api/v1/auth/login`
- `/uploads/*`

## Proteção de Rotas

### Usando Dependências

**Usuário autenticado:**
```python
from app.src.auth.dependencies import get_current_active_user
from app.src.auth.models import User

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Olá {current_user.username}"}
```

**Apenas superusuários:**
```python
from app.src.auth.dependencies import get_current_superuser

@router.delete("/admin-only")
def admin_route(current_user: User = Depends(get_current_superuser)):
    return {"message": "Rota administrativa"}
```

**Usuário opcional:**
```python
from app.src.auth.dependencies import get_optional_current_user

@router.get("/optional-auth")
def optional_auth(current_user: User = Depends(get_optional_current_user)):
    if current_user:
        return {"message": f"Olá {current_user.username}"}
    return {"message": "Olá visitante"}
```

## Configuração

### Variáveis de Ambiente (.env)

```bash
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Gerar SECRET_KEY segura:**
```bash
openssl rand -hex 32
```

### Configurações no `app/core/config.py`

```python
class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

## Erros Comuns

### 401 Unauthorized
- Token ausente ou inválido
- Token expirado
- Credenciais inválidas no login

### 403 Forbidden
- Usuário inativo
- Acesso a rota administrativa sem privilégios

### 400 Bad Request
- Email ou username já cadastrado
- Senha atual incorreta
- Validação de dados falhou

## Testes

### Exemplo com cURL

**Registro:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com",
    "username": "teste123",
    "password": "senha123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste123",
    "password": "senha123"
  }'
```

**Usar Token:**
```bash
TOKEN="seu_token_aqui"

curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## Próximos Passos

- [ ] Implementar refresh tokens
- [ ] Adicionar recuperação de senha via email
- [ ] Implementar 2FA (autenticação de dois fatores)
- [ ] Adicionar rate limiting
- [ ] Logs de auditoria de login
- [ ] Integração com OAuth2 (Google, Facebook, etc)

## Referências

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/)
- [Python Jose](https://python-jose.readthedocs.io/)
- [Passlib](https://passlib.readthedocs.io/)
