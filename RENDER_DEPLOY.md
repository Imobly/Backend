# Variáveis de Ambiente para Render.com

## ⚙️ Configuração do Deploy no Render

### 📋 Variáveis de Ambiente Obrigatórias

Configure estas variáveis no painel do Render (Settings > Environment):

#### 1. **Banco de Dados**
```
DATABASE_URL
```
- **Tipo**: Database URL do PostgreSQL
- **Valor**: Será gerado automaticamente quando você criar o PostgreSQL Database no Render
- **Formato**: `postgresql://user:password@hostname:5432/database_name`
- **Como obter**: 
  1. Crie um PostgreSQL Database no Render (Free tier)
  2. Copie o "Internal Database URL" ou "External Database URL"
  3. Cole em DATABASE_URL

#### 2. **Segurança - JWT**
```
SECRET_KEY
```
- **Tipo**: Secret
- **Valor**: String aleatória e segura (mínimo 32 caracteres)
- **Como gerar**: 
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **Exemplo**: `xK9mP2vQ8wR5tY7uI3oP1aS4dF6gH8jK0lZ9xC2vB5nM`

```
ALGORITHM
```
- **Tipo**: Plain text
- **Valor**: `HS256`
- **Descrição**: Algoritmo usado para assinar tokens JWT

```
ACCESS_TOKEN_EXPIRE_MINUTES
```
- **Tipo**: Number
- **Valor**: `30` (ou `1440` para 24 horas)
- **Descrição**: Tempo de expiração do token em minutos

#### 3. **CORS - Frontend**
```
CORS_ORIGINS
```
- **Tipo**: Plain text
- **Valor**: URLs do frontend separadas por vírgula
- **Exemplos**:
  - Desenvolvimento: `http://localhost:3000,http://localhost:5173`
  - Produção: `https://seu-app.vercel.app,https://seu-dominio.com`
  - Ambos: `https://seu-app.vercel.app,http://localhost:3000`

#### 4. **Aplicação**
```
ENVIRONMENT
```
- **Tipo**: Plain text
- **Valor**: `production`

```
DEBUG
```
- **Tipo**: Boolean
- **Valor**: `false` (IMPORTANTE: nunca `true` em produção!)

```
PROJECT_NAME
```
- **Tipo**: Plain text
- **Valor**: `Imóvel Gestão API`

```
VERSION
```
- **Tipo**: Plain text
- **Valor**: `1.0.0`

```
API_V1_STR
```
- **Tipo**: Plain text
- **Valor**: `/api/v1`

```
HOST
```
- **Tipo**: Plain text
- **Valor**: `0.0.0.0`

```
UPLOAD_DIR
```
- **Tipo**: Plain text
- **Valor**: `/tmp/uploads`
- **Nota**: No Render, use `/tmp` pois é efêmero. Para produção, considere usar S3/CloudFlare R2

---

## 🚀 Configurações do Serviço no Render

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Runtime
- **Environment**: `Python 3`
- **Python Version**: `3.11.0` (ou superior)
- **Region**: `Oregon (US West)` ou o mais próximo
- **Plan**: `Free` (para começar)

---

## 📊 Criar Banco de Dados PostgreSQL no Render

1. **No Dashboard do Render**:
   - Clique em "New +" → "PostgreSQL"
   - **Name**: `imobly-db` (ou outro nome)
   - **Database**: `imovel_gestao`
   - **User**: `imovel_user` (gerado automaticamente)
   - **Region**: Mesma do Web Service (ex: Oregon)
   - **Plan**: `Free`

2. **Após criação**:
   - Copie o **Internal Database URL** (mais rápido)
   - Cole na variável `DATABASE_URL` do Web Service

3. **Rodar Migrações** (após primeiro deploy):
   ```bash
   # No Shell do Render ou localmente apontando para o banco
   alembic upgrade head
   ```

---

## ⚠️ Observações Importantes

### Arquivos Estáticos/Uploads
- ❌ **NÃO use o sistema de arquivos do Render para uploads persistentes**
- ✅ Use serviços como:
  - AWS S3
  - Cloudflare R2
  - Supabase Storage
  - Firebase Storage

### Logs
- Visualize logs em tempo real: Dashboard → Service → Logs
- Os logs são mantidos por tempo limitado no plano Free

### Health Checks
O Render fará health checks em `/` ou `/health`. Sua aplicação já tem:
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Autenticação Separada
Como você usa um serviço Auth-api separado:
```
AUTH_API_URL
```
- **Valor**: URL do serviço de autenticação
- **Exemplo**: `https://auth-api.onrender.com`

---

## 🔧 Passo a Passo Completo

### 1. Criar PostgreSQL Database
- New + → PostgreSQL
- Configure e aguarde provisionamento
- Copie Internal Database URL

### 2. Criar Web Service
- New + → Web Service
- Conecte seu repositório GitHub
- Branch: `main` (ou `develop_costta`)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Adicionar Variáveis de Ambiente
Cole todas as variáveis listadas acima em Environment

### 4. Deploy
- Clique em "Create Web Service"
- Aguarde o build e deploy (5-10 minutos)

### 5. Rodar Migrações
Após primeiro deploy bem-sucedido:
- Dashboard → Service → Shell
- Execute: `alembic upgrade head`

### 6. Testar
- Acesse: `https://seu-servico.onrender.com/health`
- Acesse: `https://seu-servico.onrender.com/api/v1/docs`

---

## 🆘 Troubleshooting

### Erro: "Could not import module main"
✅ **Corrigido!** Use `app.main:app` no Start Command

### Banco não conecta
- Verifique se DATABASE_URL está correto
- Use Internal Database URL (mais rápido)
- Certifique-se que DB e Web Service estão na mesma região

### Timeout no Deploy
- Plano Free tem limitações
- Considere otimizar requirements.txt
- Verifique logs para erros específicos

### Uploads não persistem
- Esperado! Use S3/R2 para arquivos permanentes
- `/tmp` é limpo a cada redeploy

---

## 📱 Próximos Passos

Após backend no ar:

1. **Frontend**: Deploy no Vercel/Netlify
2. **Auth-API**: Deploy separado no Render
3. **Storage**: Configure S3/R2 para uploads
4. **Domínio**: Configure domínio customizado
5. **CI/CD**: Configure deploy automático do GitHub

---

## 🔗 URLs Importantes

- Dashboard Render: https://dashboard.render.com
- Documentação: https://render.com/docs
- Status: https://status.render.com
