# 🔑 Compartilhamento de SECRET_KEY entre Backend e Auth-API

## 📋 Arquitetura

```
┌─────────────────┐         ┌─────────────────┐
│   Auth-API      │         │    Backend      │
│  (gera tokens)  │         │ (valida tokens) │
│                 │         │                 │
│  SECRET_KEY ────┼────────►│  SECRET_KEY     │
│  (mesma chave)  │         │  (mesma chave)  │
└─────────────────┘         └─────────────────┘
```

**IMPORTANTE**: Ambos os serviços **DEVEM** usar a **MESMA** `SECRET_KEY` para:
- Auth-API: **Gerar** tokens JWT
- Backend: **Validar** tokens JWT

Se as chaves forem diferentes, o Backend não conseguirá validar os tokens gerados pelo Auth-API.

---

## 🚀 Configuração no Render

### **Passo 1: Backend já está rodando**

Se o seu Backend já está no Render e a SECRET_KEY foi gerada automaticamente:

1. Acesse: https://dashboard.render.com
2. Clique no serviço **imobly-backend**
3. Vá em **Environment**
4. Encontre a variável `SECRET_KEY`
5. **Copie o valor** (exemplo: `abc123xyz...`)

### **Passo 2: Usar a mesma chave no Auth-API**

Quando for fazer deploy do Auth-API:

1. Acesse: https://dashboard.render.com
2. Clique no serviço **auth-api** (ou crie um novo)
3. Vá em **Environment**
4. Adicione a variável:
   ```
   SECRET_KEY=<COLE_A_MESMA_CHAVE_DO_BACKEND_AQUI>
   ```

---

## 🔧 Configuração Local

### **Backend** (`.env`):
```bash
SECRET_KEY=Rys8_HKBXH9stpwcJC6GcT_SSbXxP_a1MdcggPjKUz4
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **Auth-API** (`.env`):
```bash
SECRET_KEY=Rys8_HKBXH9stpwcJC6GcT_SSbXxP_a1MdcggPjKUz4  # ⚠️ MESMA CHAVE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ✅ Checklist

- [ ] Backend no Render com SECRET_KEY configurada
- [ ] Copiar SECRET_KEY do Backend
- [ ] Auth-API no Render com a MESMA SECRET_KEY
- [ ] Testar: Auth-API gera token → Backend valida token

---

## 🧪 Como Testar

### 1. Gerar token no Auth-API:
```bash
curl -X POST https://auth-api.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"senha123"}'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 2. Usar token no Backend:
```bash
curl https://imobly-backend.onrender.com/api/v1/properties \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Deve funcionar** ✅

---

## ⚠️ Troubleshooting

### ❌ Erro: "Could not validate credentials"
**Causa**: SECRET_KEY diferente entre Auth-API e Backend

**Solução**:
1. Verifique se as chaves são EXATAMENTE iguais
2. Não deve ter espaços antes/depois
3. Case-sensitive (maiúsculas/minúsculas importam)

### ❌ Erro: "Invalid token"
**Causa**: ALGORITHM diferente

**Solução**: Ambos devem usar `ALGORITHM=HS256`

---

## 🔐 Segurança

### ❌ NÃO faça:
- Commitar SECRET_KEY no código
- Usar chaves diferentes em dev/prod
- Compartilhar a chave publicamente

### ✅ FAÇA:
- Usar variáveis de ambiente
- Mesma chave em todos os serviços que validam JWT
- Rotacionar a chave periodicamente (mas trocar em TODOS os serviços)

---

## 📝 Resumo

| Serviço   | Função           | SECRET_KEY         |
|-----------|------------------|--------------------|
| Auth-API  | Gera tokens JWT  | `abc123xyz...`     |
| Backend   | Valida tokens    | `abc123xyz...` ⚠️ MESMA |

**Regra de Ouro**: 🔑 **UMA chave para todos os serviços que compartilham autenticação**
