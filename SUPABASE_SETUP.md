# 🗄️ Configuração Supabase Database

## ✅ Credenciais do Banco

**Connection String (Connection Pooling - Recomendado)**:
```
postgresql://postgres.yyeldattafklyutbbnhu:[YOUR_PASSWORD]@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**Connection String (Direct Connection)**:
```
postgresql://postgres.yyeldattafklyutbbnhu:[YOUR_PASSWORD]@aws-0-us-west-2.pooler.supabase.com:6543/postgres
```

---

## 🔧 Configuração Local (.env)

### 1. Crie o arquivo `.env` na raiz do projeto

```bash
cp .env.example .env
```

### 2. Edite o `.env` com suas credenciais

```dotenv
# ============================================
# PRODUCTION (Supabase)
# ============================================
DATABASE_URL=postgresql://postgres.yyeldattafklyutbbnhu:SUA_SENHA_AQUI@aws-0-us-west-2.pooler.supabase.com:5432/postgres

# ============================================
# Application Settings
# ============================================
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME=Imóvel Gestão API
VERSION=1.0.0
API_V1_STR=/api/v1
HOST=0.0.0.0
PORT=8000

# ============================================
# CORS Settings
# ============================================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ============================================
# JWT/Security Configuration
# ============================================
# IMPORTANTE: Gere uma nova chave:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=GERE_UMA_CHAVE_SEGURA_AQUI
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# Upload/Storage
# ============================================
UPLOAD_DIR=./uploads
```

### 3. **IMPORTANTE**: Substitua `SUA_SENHA_AQUI` pela senha real do Supabase

---

## 🚀 Rodar Migrações no Supabase

### Opção 1: Usando Alembic (Recomendado)

```bash
# 1. Certifique-se que .env está configurado com DATABASE_URL do Supabase
# 2. Rode as migrações
alembic upgrade head
```

### Opção 2: Executar SQL Manualmente no Supabase

1. Acesse: https://supabase.com/dashboard
2. Vá em: Project → SQL Editor
3. Execute o SQL de criação de tabelas:

```sql
-- Criar schema (se necessário)
CREATE SCHEMA IF NOT EXISTS public;

-- Ver arquivos de migração em: migrations/versions/
-- Execute cada arquivo .py convertido para SQL ou use Alembic
```

---

## 🔐 Obter Senha do Supabase

### Se você perdeu a senha:

1. **Dashboard Supabase**: https://supabase.com/dashboard
2. **Project Settings** → **Database**
3. **Reset Database Password**
4. ⚠️ **Cuidado**: Isso invalida todas as conexões existentes!

### Se você tem a senha:

- Cole direto na `DATABASE_URL`
- ⚠️ **Nunca commite a senha no Git!**

---

## 🌍 Configurar Variáveis no Render

### 1. No Dashboard do Render:
- Vá em: **Environment** (aba lateral)

### 2. Adicione:

```bash
DATABASE_URL = postgresql://postgres.yyeldattafklyutbbnhu:SUA_SENHA@aws-0-us-west-2.pooler.supabase.com:5432/postgres
SECRET_KEY = <Gere: python -c "import secrets; print(secrets.token_urlsafe(32))">
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CORS_ORIGINS = https://seu-frontend.vercel.app
ENVIRONMENT = production
DEBUG = false
PROJECT_NAME = Imóvel Gestão API
VERSION = 1.0.0
API_V1_STR = /api/v1
HOST = 0.0.0.0
UPLOAD_DIR = /tmp/uploads
```

### 3. Salve e Redeploy

---

## ✅ Testar Conexão

### Teste Local:

```bash
# 1. Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# 2. Teste a conexão
python -c "from app.db.session import engine; print('✅ Conectado:', engine.url)"

# 3. Rode a aplicação
uvicorn app.main:app --reload
```

### Acesse:
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/api/v1/docs

---

## 🗄️ Diferenças Connection Pooling vs Direct

| Característica | Connection Pooling (Porta 5432) | Direct Connection (Porta 6543) |
|----------------|----------------------------------|--------------------------------|
| **Uso** | Produção (Render, Vercel) | Dev local, CLI, Migrations |
| **Performance** | ⚡ Alta (pool reutilizável) | 🐢 Média (1 conexão) |
| **Limite** | 15 conexões (Free tier) | Ilimitado |
| **Recomendado** | ✅ Sim para aplicações web | ⚠️ Apenas para admin |

**Use Connection Pooling (porta 5432)** para Render/produção!

---

## 🔧 Troubleshooting

### ❌ Erro: "password authentication failed"
- Verifique se a senha está correta
- Certifique-se de URL-encode caracteres especiais na senha
- Exemplo: `p@ssw0rd` → `p%40ssw0rd`

### ❌ Erro: "too many connections"
- Você está usando Direct Connection (6543) em produção
- **Solução**: Use Connection Pooling (porta 5432)

### ❌ Erro: "SSL required"
- Adicione `?sslmode=require` ao final da URL:
```
postgresql://...postgres?sslmode=require
```

### ❌ Tabelas não existem
- Rode as migrações: `alembic upgrade head`
- Ou execute SQL manualmente no Supabase SQL Editor

---

## 📊 Gerenciar Banco pelo Supabase Dashboard

### Ver Tabelas:
1. Dashboard → **Table Editor**
2. Veja todas as tabelas criadas

### Executar SQL:
1. Dashboard → **SQL Editor**
2. Execute queries customizadas

### Ver Logs:
1. Dashboard → **Logs**
2. Veja queries executadas

### Backups:
1. Dashboard → **Database** → **Backups**
2. Plano Free: Backups diários (7 dias)

---

## 🔄 Migração de Dados (se necessário)

Se você tem dados locais para migrar:

### 1. Exportar do PostgreSQL Local:
```bash
pg_dump -U postgres -d imovel_gestao > backup.sql
```

### 2. Importar para Supabase:
```bash
psql "postgresql://postgres.yyeldattafklyutbbnhu:SENHA@aws-0-us-west-2.pooler.supabase.com:6543/postgres" < backup.sql
```

---

## 📝 Checklist de Deploy

- [ ] DATABASE_URL configurada no `.env` local
- [ ] SECRET_KEY gerada (nova e segura)
- [ ] Migrações rodadas: `alembic upgrade head`
- [ ] Teste local funcionando: `uvicorn app.main:app`
- [ ] DATABASE_URL configurada no Render
- [ ] CORS_ORIGINS atualizado com URL do frontend
- [ ] Deploy feito no Render
- [ ] Teste produção: `https://seu-app.onrender.com/health`

---

## 🆘 Suporte

- **Supabase Docs**: https://supabase.com/docs/guides/database
- **Render Docs**: https://render.com/docs/databases
- **FastAPI + Postgres**: https://fastapi.tiangolo.com/tutorial/sql-databases/

---

## 🔗 Links Úteis

- **Supabase Dashboard**: https://supabase.com/dashboard
- **Render Dashboard**: https://dashboard.render.com
- **Seu Projeto (Supabase)**: https://supabase.com/dashboard/project/yyeldattafklyutbbnhu
