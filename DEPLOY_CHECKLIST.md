# 🚀 Configuração Render - Guia Rápido

## ✅ Pré-requisitos Completos

✔️ Banco Supabase configurado  
✔️ Senha do banco: `Imobly.1501`  
✔️ SECRET_KEY gerada: `Rys8_HKBXH9stpwcJC6GcT_SSbXxP_a1MdcggPjKUz4`  
✔️ Código pronto para deploy (branch `develop_costta` ou `main`)

---

## 📋 Variáveis de Ambiente para o Render

Copie e cole EXATAMENTE estas variáveis no Render Dashboard → Environment:

```bash
PYTHON_VERSION=3.11.0
DATABASE_URL=postgresql://postgres.yyeldattafklyutbbnhu:Imobly.1501@aws-0-us-west-2.pooler.supabase.com:5432/postgres
SECRET_KEY=Rys8_HKBXH9stpwcJC6GcT_SSbXxP_a1MdcggPjKUz4
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME=Imóvel Gestão API
VERSION=1.0.0
API_V1_STR=/api/v1
HOST=0.0.0.0
UPLOAD_DIR=/tmp/uploads
```

---

## 🔧 Configuração do Web Service

### Build Settings:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### General:
- **Environment**: `Python 3`
- **Python Version**: `3.11.0` (configure na variável PYTHON_VERSION)
- **Branch**: `main` (ou `develop_costta` para teste)
- **Region**: `Oregon (US West)` (mesma do Supabase)
- **Plan**: `Free`

---

## ✅ Checklist de Deploy

- [ ] Repositório no GitHub atualizado
- [ ] Branch `main` ou `develop_costta` com último commit
- [ ] Web Service criado no Render
- [ ] Todas as 12 variáveis de ambiente configuradas
- [ ] Build Command correto: `pip install -r requirements.txt`
- [ ] Start Command correto: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Deploy iniciado (aguardar 5-10 minutos)

---

## 🧪 Testar Após Deploy

Acesse estas URLs (substitua `seu-app` pelo nome real):

### 1. Health Check:
```
https://seu-app.onrender.com/health
```
**Resposta esperada**:
```json
{"status": "healthy", "service": "Imóvel Gestão API"}
```

### 2. API Docs (Swagger):
```
https://seu-app.onrender.com/api/v1/docs
```
**Deve abrir**: Interface Swagger UI com todos os endpoints

### 3. Root:
```
https://seu-app.onrender.com/
```
**Resposta esperada**:
```json
{
  "message": "Bem-vindo ao Imóvel Gestão API",
  "version": "1.0.0",
  "docs": "/docs",
  "api": "/api/v1"
}
```

---

## ⚠️ Troubleshooting

### ❌ Build falhou
- Verifique se `requirements.txt` está no repositório
- Confira logs: Dashboard → Service → Logs

### ❌ Erro: "Could not import module main"
✅ **JÁ CORRIGIDO** - Start Command usa `app.main:app`

### ❌ Erro de conexão com banco
- Verifique se DATABASE_URL está correta
- Use Connection Pooling (porta 5432) ✅
- Teste conexão no Supabase Dashboard

### ❌ Deploy lento (>10 minutos)
- Normal no plano Free
- Render coloca serviços para "dormir" após inatividade

---

## 📝 Próximos Passos

### Após primeiro deploy bem-sucedido:

1. **Configure CORS** (quando tiver frontend):
   - No código `app/core/config.py`, adicione URL do frontend em `CORS_ORIGINS`
   - Ou adicione variável `CORS_ORIGINS` no Render (não necessário agora)

2. **Domínio Customizado** (opcional):
   - Dashboard → Settings → Custom Domain
   - Configure DNS no seu provedor

3. **Auto Deploy**:
   - Dashboard → Settings → Build & Deploy
   - Enable "Auto-Deploy: Yes"
   - Cada push para `main` fará deploy automático

4. **Monitoramento**:
   - Dashboard → Logs (tempo real)
   - Dashboard → Metrics (uso de recursos)

---

## 🔗 Links Importantes

- **Render Dashboard**: https://dashboard.render.com
- **Supabase Dashboard**: https://supabase.com/dashboard/project/yyeldattafklyutbbnhu
- **GitHub Repo**: https://github.com/Imobly/Backend

---

## 📞 Suporte

- **Documentação Render**: https://render.com/docs
- **Documentação Supabase**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## ✨ Resumo

Tudo está configurado corretamente:
- ✅ Arquivos `.env` organizados (apenas `.env` e `.env.example`)
- ✅ `render.yaml` com todas as variáveis
- ✅ Banco Supabase conectado
- ✅ SECRET_KEY gerada e segura
- ✅ Código pronto para deploy

**Agora é só fazer deploy no Render!** 🚀
