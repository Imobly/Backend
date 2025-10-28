# 📡 API Endpoints - Referência Completa

Documentação completa de todos os endpoints da API Imóvel Gestão.

**Base URL:** `http://localhost:8000/api/v1`

## 📋 Tabela de Referência Rápida

| Módulo | Método | Endpoint | Descrição | Auth |
|--------|--------|----------|-----------|------|
| **Autenticação** |
| Auth | POST | `/auth/register` | Criar nova conta | ❌ |
| Auth | POST | `/auth/login` | Login (obtém token JWT) | ❌ |
| Auth | GET | `/auth/me` | Dados do usuário atual | ✅ |
| Auth | PUT | `/auth/me` | Atualizar dados do usuário | ✅ |
| Auth | POST | `/auth/change-password` | Alterar senha | ✅ |
| Auth | GET | `/auth/users` | Listar todos os usuários | ✅ (Admin) |
| Auth | GET | `/auth/users/{id}` | Obter usuário por ID | ✅ (Admin) |
| Auth | DELETE | `/auth/users/{id}` | Deletar usuário | ✅ (Admin) |
| **Propriedades** |
| Properties | GET | `/properties` | Listar propriedades | ✅ |
| Properties | POST | `/properties` | Criar propriedade | ✅ |
| Properties | GET | `/properties/{id}` | Obter propriedade | ✅ |
| Properties | PUT | `/properties/{id}` | Atualizar propriedade | ✅ |
| Properties | DELETE | `/properties/{id}` | Deletar propriedade | ✅ |
| Properties | GET | `/properties/status/{status}` | Filtrar por status | ✅ |
| Properties | GET | `/properties/type/{type}` | Filtrar por tipo | ✅ |
| **Inquilinos** |
| Tenants | GET | `/tenants` | Listar inquilinos | ✅ |
| Tenants | POST | `/tenants` | Criar inquilino | ✅ |
| Tenants | GET | `/tenants/{id}` | Obter inquilino | ✅ |
| Tenants | PUT | `/tenants/{id}` | Atualizar inquilino | ✅ |
| Tenants | DELETE | `/tenants/{id}` | Deletar inquilino | ✅ |
| Tenants | GET | `/tenants/cpf/{cpf}` | Buscar por CPF/CNPJ | ✅ |
| Tenants | GET | `/tenants/search` | Buscar por query | ✅ |
| **Unidades** |
| Units | GET | `/units` | Listar unidades | ✅ |
| Units | POST | `/units` | Criar unidade | ✅ |
| Units | GET | `/units/{id}` | Obter unidade | ✅ |
| Units | PUT | `/units/{id}` | Atualizar unidade | ✅ |
| Units | DELETE | `/units/{id}` | Deletar unidade | ✅ |
| Units | GET | `/units/property/{property_id}` | Unidades de propriedade | ✅ |
| **Contratos** |
| Contracts | GET | `/contracts` | Listar contratos | ✅ |
| Contracts | POST | `/contracts` | Criar contrato | ✅ |
| Contracts | GET | `/contracts/{id}` | Obter contrato | ✅ |
| Contracts | PUT | `/contracts/{id}` | Atualizar contrato | ✅ |
| Contracts | DELETE | `/contracts/{id}` | Deletar contrato | ✅ |
| Contracts | GET | `/contracts/status/{status}` | Filtrar por status | ✅ |
| Contracts | GET | `/contracts/property/{property_id}` | Contratos de propriedade | ✅ |
| Contracts | GET | `/contracts/tenant/{tenant_id}` | Contratos de inquilino | ✅ |
| **Pagamentos** |
| Payments | GET | `/payments` | Listar pagamentos | ✅ |
| Payments | POST | `/payments` | Criar pagamento | ✅ |
| Payments | GET | `/payments/{id}` | Obter pagamento | ✅ |
| Payments | PUT | `/payments/{id}` | Atualizar pagamento | ✅ |
| Payments | DELETE | `/payments/{id}` | Deletar pagamento | ✅ |
| Payments | GET | `/payments/status/{status}` | Filtrar por status | ✅ |
| Payments | GET | `/payments/contract/{contract_id}` | Pagamentos de contrato | ✅ |
| **Despesas** |
| Expenses | GET | `/expenses` | Listar despesas | ✅ |
| Expenses | POST | `/expenses` | Criar despesa | ✅ |
| Expenses | GET | `/expenses/{id}` | Obter despesa | ✅ |
| Expenses | PUT | `/expenses/{id}` | Atualizar despesa | ✅ |
| Expenses | DELETE | `/expenses/{id}` | Deletar despesa | ✅ |
| Expenses | GET | `/expenses/property/{property_id}` | Despesas de propriedade | ✅ |
| Expenses | GET | `/expenses/category/{category}` | Filtrar por categoria | ✅ |
| Expenses | GET | `/expenses/monthly` | Estatísticas mensais | ✅ |
| **Notificações** |
| Notifications | GET | `/notifications` | Listar notificações | ✅ |
| Notifications | POST | `/notifications` | Criar notificação | ✅ |
| Notifications | GET | `/notifications/{id}` | Obter notificação | ✅ |
| Notifications | PUT | `/notifications/{id}/read` | Marcar como lida | ✅ |
| Notifications | DELETE | `/notifications/{id}` | Deletar notificação | ✅ |
| Notifications | GET | `/notifications/unread` | Notificações não lidas | ✅ |
| **Dashboard** |
| Dashboard | GET | `/dashboard/summary` | Resumo geral | ✅ |
| Dashboard | GET | `/dashboard/revenue` | Receitas mensais | ✅ |
| Dashboard | GET | `/dashboard/expenses` | Despesas mensais | ✅ |
| Dashboard | GET | `/dashboard/properties` | Estatísticas de propriedades | ✅ |
| Dashboard | GET | `/dashboard/recent-activity` | Atividades recentes | ✅ |

**Legenda:**
- ✅ = Requer autenticação (Bearer Token)
- ❌ = Endpoint público
- ✅ (Admin) = Requer permissões de administrador

---

## 📝 Detalhamento dos Endpoints

### 1. Autenticação

#### POST /auth/register
Criar uma nova conta de usuário.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword123",
  "full_name": "Full Name"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-28T10:00:00"
}
```

**Erros:**
- `400` - Email ou username já existem
- `422` - Dados de validação inválidos

---

#### POST /auth/login
Autenticar usuário e obter token JWT.

**Request Body:**
```json
{
  "username": "username",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erros:**
- `401` - Credenciais inválidas
- `403` - Usuário inativo

---

#### GET /auth/me
Obter informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-28T10:00:00"
}
```

**Erros:**
- `401` - Token inválido ou expirado

---

#### PUT /auth/me
Atualizar informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "full_name": "New Full Name"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "username": "username",
  "full_name": "New Full Name",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-28T10:00:00"
}
```

---

#### POST /auth/change-password
Alterar senha do usuário autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

**Response (200 OK):**
```json
{
  "message": "Senha alterada com sucesso"
}
```

**Erros:**
- `400` - Senha atual incorreta

---

### 2. Propriedades

#### GET /properties
Listar todas as propriedades com paginação e filtros opcionais.

**Query Parameters:**
- `skip` (int, default=0) - Número de registros a pular
- `limit` (int, default=100) - Número máximo de registros
- `status` (string, optional) - Filtrar por status (vacant, occupied, maintenance, inactive)
- `type` (string, optional) - Filtrar por tipo (apartment, house, commercial, studio)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Edifício Central",
    "address": "Rua Principal, 123",
    "neighborhood": "Centro",
    "city": "São Paulo",
    "state": "SP",
    "zip_code": "01000-000",
    "type": "apartment",
    "area": 85.5,
    "bedrooms": 2,
    "bathrooms": 1,
    "parking_spaces": 1,
    "rent": 1500.00,
    "status": "occupied",
    "description": "Apartamento bem localizado",
    "images": ["url1.jpg", "url2.jpg"],
    "is_residential": true,
    "tenant": "João Silva",
    "created_at": "2025-01-15T10:00:00",
    "updated_at": "2025-01-15T10:00:00"
  }
]
```

---

#### POST /properties
Criar uma nova propriedade.

**Request Body:**
```json
{
  "name": "Edifício Central",
  "address": "Rua Principal, 123",
  "neighborhood": "Centro",
  "city": "São Paulo",
  "state": "SP",
  "zip_code": "01000-000",
  "type": "apartment",
  "area": 85.5,
  "bedrooms": 2,
  "bathrooms": 1,
  "parking_spaces": 1,
  "rent": 1500.00,
  "status": "vacant",
  "description": "Apartamento bem localizado",
  "images": ["url1.jpg", "url2.jpg"],
  "is_residential": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Edifício Central",
  // ... (todos os campos)
}
```

---

#### GET /properties/{id}
Obter uma propriedade específica por ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Edifício Central",
  // ... (todos os campos)
}
```

**Erros:**
- `404` - Propriedade não encontrada

---

#### PUT /properties/{id}
Atualizar uma propriedade existente.

**Request Body:** (todos os campos opcionais)
```json
{
  "rent": 1600.00,
  "status": "occupied",
  "tenant": "Maria Santos"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Edifício Central",
  "rent": 1600.00,
  "status": "occupied",
  // ... (todos os campos)
}
```

---

#### DELETE /properties/{id}
Deletar uma propriedade.

**Response (200 OK):**
```json
{
  "message": "Propriedade deletada com sucesso"
}
```

**Erros:**
- `404` - Propriedade não encontrada

---

### 3. Inquilinos

#### GET /tenants
Listar todos os inquilinos.

**Query Parameters:**
- `skip` (int, default=0)
- `limit` (int, default=100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "full_name": "João Silva",
    "email": "joao@example.com",
    "phone": "(11) 98765-4321",
    "cpf_cnpj": "123.456.789-00",
    "birth_date": "1990-05-15",
    "address": "Rua A, 100",
    "occupation": "Engenheiro",
    "monthly_income": 5000.00,
    "created_at": "2025-01-10T10:00:00",
    "updated_at": "2025-01-10T10:00:00"
  }
]
```

---

#### POST /tenants
Criar um novo inquilino.

**Request Body:**
```json
{
  "full_name": "João Silva",
  "email": "joao@example.com",
  "phone": "(11) 98765-4321",
  "cpf_cnpj": "123.456.789-00",
  "birth_date": "1990-05-15",
  "address": "Rua A, 100",
  "occupation": "Engenheiro",
  "monthly_income": 5000.00
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "full_name": "João Silva",
  // ... (todos os campos)
}
```

**Erros:**
- `400` - CPF/CNPJ já cadastrado

---

#### GET /tenants/cpf/{cpf}
Buscar inquilino por CPF ou CNPJ.

**Exemplo:** `/tenants/cpf/12345678900`

**Response (200 OK):**
```json
{
  "id": 1,
  "full_name": "João Silva",
  "cpf_cnpj": "123.456.789-00",
  // ... (todos os campos)
}
```

**Erros:**
- `404` - Inquilino não encontrado

---

#### GET /tenants/search
Buscar inquilinos por nome ou email.

**Query Parameters:**
- `q` (string, required) - Termo de busca

**Exemplo:** `/tenants/search?q=joão`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "full_name": "João Silva",
    // ... (todos os campos)
  }
]
```

---

### 4. Contratos

#### GET /contracts
Listar todos os contratos.

**Query Parameters:**
- `skip` (int)
- `limit` (int)
- `status` (string) - active, pending, expired, cancelled
- `property_id` (int)
- `tenant_id` (int)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "property_id": 1,
    "tenant_id": 1,
    "start_date": "2025-01-01",
    "end_date": "2026-01-01",
    "rent_amount": 1500.00,
    "rent_due_day": 10,
    "deposit_amount": 1500.00,
    "status": "active",
    "created_at": "2025-01-01T10:00:00",
    "updated_at": "2025-01-01T10:00:00"
  }
]
```

---

#### POST /contracts
Criar um novo contrato.

**Request Body:**
```json
{
  "property_id": 1,
  "tenant_id": 1,
  "start_date": "2025-01-01",
  "end_date": "2026-01-01",
  "rent_amount": 1500.00,
  "rent_due_day": 10,
  "deposit_amount": 1500.00,
  "status": "active"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "property_id": 1,
  // ... (todos os campos)
}
```

---

### 5. Pagamentos

#### GET /payments
Listar todos os pagamentos.

**Query Parameters:**
- `skip` (int)
- `limit` (int)
- `status` (string) - pending, paid, overdue, partial
- `contract_id` (int)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "contract_id": 1,
    "tenant_id": 1,
    "property_id": 1,
    "amount": 1500.00,
    "due_date": "2025-02-10",
    "payment_date": "2025-02-08",
    "status": "paid",
    "payment_method": "pix",
    "fine_amount": 0.00,
    "description": "Aluguel Fevereiro/2025",
    "created_at": "2025-02-01T10:00:00",
    "updated_at": "2025-02-08T15:30:00"
  }
]
```

---

#### POST /payments
Criar um novo pagamento.

**Request Body:**
```json
{
  "contract_id": 1,
  "tenant_id": 1,
  "property_id": 1,
  "amount": 1500.00,
  "due_date": "2025-02-10",
  "payment_method": "pix",
  "description": "Aluguel Fevereiro/2025"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "contract_id": 1,
  // ... (todos os campos)
}
```

---

### 6. Despesas

#### GET /expenses
Listar todas as despesas.

**Query Parameters:**
- `skip` (int)
- `limit` (int)
- `property_id` (int)
- `category` (string) - maintenance, tax, utility, insurance, other
- `month` (int)
- `year` (int)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "property_id": 1,
    "description": "Manutenção do elevador",
    "amount": 500.00,
    "category": "maintenance",
    "expense_date": "2025-02-05",
    "paid": true,
    "created_at": "2025-02-05T10:00:00",
    "updated_at": "2025-02-05T10:00:00"
  }
]
```

---

#### POST /expenses
Criar uma nova despesa.

**Request Body:**
```json
{
  "property_id": 1,
  "description": "Manutenção do elevador",
  "amount": 500.00,
  "category": "maintenance",
  "expense_date": "2025-02-05",
  "paid": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "property_id": 1,
  // ... (todos os campos)
}
```

---

### 7. Dashboard

#### GET /dashboard/summary
Obter resumo geral do sistema.

**Response (200 OK):**
```json
{
  "total_properties": 50,
  "total_contracts": 45,
  "active_contracts": 42,
  "occupancy_rate": 84.0,
  "monthly_revenue": 67500.00,
  "monthly_expenses": 15000.00,
  "net_profit": 52500.00,
  "overdue_payments": 3,
  "expiring_contracts": 5,
  "unread_notifications": 10
}
```

---

#### GET /dashboard/revenue
Obter receitas mensais.

**Query Parameters:**
- `year` (int, required)
- `month` (int, optional)

**Response (200 OK):**
```json
{
  "year": 2025,
  "month": 2,
  "total_revenue": 67500.00,
  "paid_revenue": 65000.00,
  "pending_revenue": 2500.00,
  "overdue_revenue": 0.00
}
```

---

## 🔒 Autenticação

Todos os endpoints (exceto `/auth/register` e `/auth/login`) requerem autenticação via Bearer Token.

**Como usar:**

1. Obter token via `/auth/login`
2. Incluir em todas as requisições:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Exemplos:**

```bash
# cURL
curl -H "Authorization: Bearer {token}" http://localhost:8000/api/v1/properties

# JavaScript
fetch('http://localhost:8000/api/v1/properties', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})

# Python
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/v1/properties', headers=headers)
```

---

## 📊 Códigos de Status HTTP

| Código | Significado | Quando ocorre |
|--------|-------------|---------------|
| 200 | OK | Requisição bem-sucedida (GET, PUT, DELETE) |
| 201 | Created | Recurso criado com sucesso (POST) |
| 400 | Bad Request | Dados inválidos ou regra de negócio violada |
| 401 | Unauthorized | Token ausente, inválido ou expirado |
| 403 | Forbidden | Sem permissões para acessar o recurso |
| 404 | Not Found | Recurso não encontrado |
| 422 | Unprocessable Entity | Erro de validação (Pydantic) |
| 500 | Internal Server Error | Erro no servidor |

---

## 🧪 Testando a API

### Swagger UI (Recomendado)
Acesse: http://localhost:8000/docs

Interface interativa para testar todos os endpoints.

### ReDoc
Acesse: http://localhost:8000/redoc

Documentação alternativa, melhor para leitura.

### Postman/Insomnia
Importe a coleção OpenAPI:
```
http://localhost:8000/openapi.json
```

---

**Última atualização:** Outubro 2025
