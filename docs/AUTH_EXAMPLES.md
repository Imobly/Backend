# Exemplos de Uso da API de Autenticação

## Fluxo Completo de Autenticação

### 1. Registrar Novo Usuário

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "username": "joaosilva",
    "password": "senha@123",
    "full_name": "João Silva"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "email": "joao@example.com",
  "username": "joaosilva",
  "full_name": "João Silva",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-27T23:30:00"
}
```

### 2. Fazer Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joaosilva",
    "password": "senha@123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJqb2Fvc2lsdmEiLCJleHAiOjE3MzAxMjM0MDB9.abc123...",
  "token_type": "bearer"
}
```

### 3. Usar Token em Requisições

Salve o token em uma variável para facilitar:

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Obter Dados do Usuário Atual

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Atualizar Perfil

```bash
curl -X PUT http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "João Pedro Silva"
  }'
```

### 6. Alterar Senha

```bash
curl -X POST http://localhost:8000/api/v1/auth/change-password \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "senha@123",
    "new_password": "novasenha@456"
  }'
```

## Usando a Autenticação com Outras APIs

### Criar Propriedade (Requer Autenticação)

```bash
curl -X POST http://localhost:8000/api/v1/properties \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Apartamento Centro",
    "address": "Rua Principal, 123",
    "city": "São Paulo",
    "state": "SP",
    "type": "apartment",
    "rent": 2500.00,
    "status": "vacant"
  }'
```

### Listar Propriedades (Requer Autenticação)

```bash
curl -X GET http://localhost:8000/api/v1/properties \
  -H "Authorization: Bearer $TOKEN"
```

## Exemplo Python com Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# 1. Registrar usuário
register_data = {
    "email": "maria@example.com",
    "username": "mariasilva",
    "password": "senha@123",
    "full_name": "Maria Silva"
}

response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print("Registro:", response.json())

# 2. Fazer login
login_data = {
    "username": "mariasilva",
    "password": "senha@123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token_data = response.json()
token = token_data["access_token"]
print("Token:", token)

# 3. Criar headers com token
headers = {
    "Authorization": f"Bearer {token}"
}

# 4. Usar API autenticada
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print("Meu perfil:", response.json())

# 5. Criar propriedade
property_data = {
    "name": "Casa na Praia",
    "address": "Av. Beira Mar, 456",
    "city": "Santos",
    "state": "SP",
    "type": "house",
    "rent": 5000.00,
    "status": "vacant"
}

response = requests.post(f"{BASE_URL}/properties", headers=headers, json=property_data)
print("Propriedade criada:", response.json())
```

## Exemplo JavaScript/TypeScript

```javascript
// Configuração
const BASE_URL = 'http://localhost:8000/api/v1';

// 1. Registrar usuário
async function register() {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'pedro@example.com',
      username: 'pedrosousa',
      password: 'senha@123',
      full_name: 'Pedro Sousa'
    })
  });
  
  return await response.json();
}

// 2. Fazer login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  // Salvar token no localStorage
  localStorage.setItem('token', data.access_token);
  return data;
}

// 3. Obter token do localStorage
function getToken() {
  return localStorage.getItem('token');
}

// 4. Fazer requisição autenticada
async function getProfile() {
  const token = getToken();
  
  const response = await fetch(`${BASE_URL}/auth/me`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
}

// 5. Criar propriedade
async function createProperty(propertyData) {
  const token = getToken();
  
  const response = await fetch(`${BASE_URL}/properties`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(propertyData)
  });
  
  return await response.json();
}

// Uso
(async () => {
  // Registrar
  await register();
  
  // Login
  const tokenData = await login('pedrosousa', 'senha@123');
  console.log('Token:', tokenData.access_token);
  
  // Ver perfil
  const profile = await getProfile();
  console.log('Perfil:', profile);
  
  // Criar propriedade
  const property = await createProperty({
    name: 'Loft Moderno',
    address: 'Rua Augusta, 789',
    city: 'São Paulo',
    state: 'SP',
    type: 'loft',
    rent: 3500.00,
    status: 'vacant'
  });
  console.log('Propriedade:', property);
})();
```

## Tratamento de Erros

### Token Expirado

Quando o token expira (padrão: 30 minutos), você receberá:

```json
{
  "detail": "Token inválido ou expirado"
}
```

**Solução:** Fazer login novamente para obter um novo token.

### Token Ausente

Se não enviar o header Authorization:

```json
{
  "detail": "Not authenticated"
}
```

### Credenciais Inválidas

```json
{
  "detail": "Credenciais inválidas"
}
```

## Boas Práticas

### 1. Armazenar Token com Segurança

- **Frontend Web**: Use `localStorage` ou `sessionStorage` (atenção: vulnerável a XSS)
- **Aplicativo Mobile**: Use armazenamento seguro (Keychain no iOS, Keystore no Android)
- **Backend**: Armazene em variável de ambiente

### 2. Renovar Token Antes de Expirar

```javascript
// Verificar se token vai expirar em breve
function isTokenExpiringSoon(token) {
  const payload = JSON.parse(atob(token.split('.')[1]));
  const expirationTime = payload.exp * 1000; // Converter para ms
  const now = Date.now();
  const fiveMinutes = 5 * 60 * 1000;
  
  return (expirationTime - now) < fiveMinutes;
}

// Renovar se necessário
if (isTokenExpiringSoon(token)) {
  await login(username, password); // Fazer login novamente
}
```

### 3. Limpar Token ao Fazer Logout

```javascript
function logout() {
  localStorage.removeItem('token');
  // Redirecionar para página de login
  window.location.href = '/login';
}
```

### 4. Interceptor de Requisições (Axios)

```javascript
import axios from 'axios';

// Adicionar token automaticamente em todas as requisições
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Tratar erro 401 (token inválido)
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expirado - fazer logout
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Middleware de Autenticação Global (Opcional)

Para habilitar autenticação obrigatória em TODAS as rotas (exceto públicas), descomente no `app/main.py`:

```python
from app.src.auth.middleware import AuthMiddleware

app.add_middleware(AuthMiddleware)
```

**Rotas públicas (não precisam de token):**
- `/`
- `/health`
- `/api/v1/docs`
- `/api/v1/redoc`
- `/api/v1/openapi.json`
- `/api/v1/auth/register`
- `/api/v1/auth/login`
- `/uploads/*`

**Todas as outras rotas exigirão o token!**
