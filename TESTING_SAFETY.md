# 🔒 GUIA DE SEGURANÇA PARA TESTES

## ⚠️ IMPORTANTE: PROTEÇÃO CONTRA PERDA DE DADOS

Os testes automatizados **criam e destroem dados** para garantir um ambiente limpo. Por isso, é **CRÍTICO** que eles rodem em um banco de dados **SEPARADO** do de produção.

## 🛡️ Proteções Implementadas

### 1. Validação Obrigatória de TEST_DATABASE_URL

O sistema agora **REJEITA** testes se:
- `TEST_DATABASE_URL` não estiver definido
- `TEST_DATABASE_URL` for igual a `DATABASE_URL` (produção)
- O nome do banco não contiver `_test` (aviso)

### 2. Schema Isolado

Os testes agora usam um **schema separado** (`test_schema`) ao invés do `public`:
- Mesmo que você acidentalmente use o mesmo banco, os dados de produção em `public` não serão afetados
- O schema `test_schema` é **destruído** após cada teste

### 3. Banco de Testes Dedicado (Docker)

Um container **separado** foi criado para testes:
- **Produção**: `postgres` (porta 5432) → `imovel_gestao`
- **Testes**: `postgres-test` (porta 5433) → `imovel_gestao_test`

## 📋 Como Rodar Testes Corretamente

### Opção 1: Script Seguro (Recomendado)

```powershell
# Windows PowerShell
.\scripts\run_tests_safe.ps1
```

Este script:
- ✅ Configura automaticamente o banco de testes
- ✅ Inicia o container postgres-test se necessário
- ✅ Roda os testes com segurança
- ✅ Mostra relatório de cobertura

### Opção 2: Manual (Local)

```powershell
# 1. Definir variável de ambiente
$env:TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5433/imovel_gestao_test"

# 2. Rodar testes
pytest tests/integration/ -v
```

### Opção 3: Docker

```powershell
# Rodar testes dentro do container backend
docker compose exec backend sh -c "TEST_DATABASE_URL=postgresql://postgres:admin123@postgres-test:5432/imovel_gestao_test pytest tests/integration/ -v"
```

## 🚀 Configuração Inicial

### 1. Criar Banco de Testes (se não usar Docker)

```sql
-- Conectar ao Postgres
psql -U postgres

-- Criar banco de testes
CREATE DATABASE imovel_gestao_test;

-- Sair
\q
```

### 2. Iniciar Containers

```powershell
# Iniciar TODOS os containers (incluindo postgres-test)
docker compose up -d

# Ou apenas o banco de testes
docker compose up -d postgres-test
```

### 3. Verificar

```powershell
# Ver containers rodando
docker compose ps

# Você deve ver:
# - imovel_postgres (porta 5432) - PRODUÇÃO
# - imovel_postgres_test (porta 5433) - TESTES
```

## ❌ O QUE NUNCA FAZER

```powershell
# ❌ NUNCA faça isso (vai tentar usar banco de produção):
pytest

# ❌ NUNCA configure TEST_DATABASE_URL igual a DATABASE_URL:
$env:TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/imovel_gestao"
```

## ✅ O QUE FAZER

```powershell
# ✅ SEMPRE use banco diferente:
$env:TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5433/imovel_gestao_test"

# ✅ Ou use o script seguro:
.\scripts\run_tests_safe.ps1
```

## 🔍 Verificar Dados Não Foram Afetados

Após rodar testes, você pode verificar que seus dados de produção estão intactos:

```powershell
# Conectar ao banco de PRODUÇÃO
docker compose exec postgres psql -U postgres -d imovel_gestao

# Verificar dados
SELECT COUNT(*) FROM properties;
SELECT COUNT(*) FROM tenants;
SELECT COUNT(*) FROM payments;

# Deve retornar os mesmos números de antes dos testes
```

## 📊 GitHub Actions / CI/CD

O GitHub Actions já está configurado para usar banco separado:

```yaml
# .github/workflows/tests.yml
env:
  TEST_DATABASE_URL: postgresql://postgres:postgres@localhost:5432/imovel_gestao_test
```

## 🆘 Em Caso de Problemas

Se você ver alguma dessas mensagens ao tentar rodar testes:

### ❌ "TEST_DATABASE_URL não está definido"
**Solução**: Configure a variável de ambiente antes de rodar testes

```powershell
$env:TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5433/imovel_gestao_test"
```

### ❌ "TEST_DATABASE_URL é igual a DATABASE_URL (produção)"
**Solução**: Use um banco diferente para testes

```powershell
# Errado:
$env:TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/imovel_gestao"

# Correto:
$env:TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5433/imovel_gestao_test"
```

### ⚠️ "O nome do banco de testes deve conter '_test'"
**Solução**: Renomeie o banco ou digite 'SIM' para continuar (não recomendado)

## 📝 Resumo das Camadas de Proteção

1. **Validação de URL**: Sistema recusa rodar sem TEST_DATABASE_URL
2. **Comparação**: Sistema recusa se TEST_DATABASE_URL == DATABASE_URL
3. **Nomenclatura**: Aviso se o nome não contém '_test'
4. **Schema Isolado**: Usa 'test_schema' ao invés de 'public'
5. **Container Dedicado**: postgres-test separado do postgres

Com essas proteções, é **praticamente impossível** apagar dados de produção acidentalmente! 🛡️
