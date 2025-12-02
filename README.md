# 🏢 Imobly Backend API

API REST para gestão de propriedades imobiliárias, inquilinos, contratos e pagamentos.

## 🌐 Ambiente de Produção

- **API Backend**: https://backend-non0.onrender.com
- **API de Autenticação**: https://auth-api-3zxk.onrender.com
- **Frontend**: https://imobly.onrender.com
- **Documentação Completa**: https://imobly.github.io/Documentation/
- **Swagger/OpenAPI**: https://backend-non0.onrender.com/api/v1/docs

---

## 🚀 Funcionalidades

### 📋 Gestão de Propriedades
- ✅ Cadastro, listagem, edição e exclusão de imóveis
- ✅ Gerenciamento de unidades (apartamentos, salas comerciais)
- ✅ Suporte para diferentes tipos: apartamento, casa, comercial, studio
- ✅ Controle de status: vago, ocupado, manutenção, inativo

### 👥 Gestão de Inquilinos
- ✅ Cadastro completo com CPF/CNPJ
- ✅ Validação de email e documentos
- ✅ Histórico de contratos e pagamentos
- ✅ Status: ativo, inativo

### 📝 Gestão de Contratos
- ✅ Contratos de locação com datas de início e fim
- ✅ Valores de aluguel, depósito e taxas
- ✅ Status: ativo, expirado, terminado
- ✅ Geração automática de parcelas de pagamento

### 💰 Gestão de Pagamentos
- ✅ Registro de pagamentos com múltiplos métodos
- ✅ Cálculo automático de multa e juros por atraso
- ✅ Status: pendente, pago, atrasado, parcial
- ✅ Relatórios e histórico de pagamentos

### 💸 Gestão de Despesas
- ✅ Registro de despesas relacionadas às propriedades
- ✅ Categorização por tipo
- ✅ Anexo de comprovantes

### 🔔 Notificações
- ✅ Notificações automáticas de eventos
- ✅ Alertas de pagamentos próximos ao vencimento
- ✅ Confirmações de ações realizadas

---

## 🛠️ Tecnologias

- **Python 3.11**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** (Produção: Supabase)
- **JWT** - Autenticação via tokens
- **Pytest** - Testes automatizados
- **Docker** - Containerização

---

## 📦 Instalação e Execução Local

### Pré-requisitos

- Python 3.11+
- PostgreSQL (ou Docker)
- Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/Imobly/Backend.git
cd Backend/Backend
```

### 2. Criar Ambiente Virtual

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Database (use PostgreSQL local ou Docker)
DATABASE_URL=postgresql://postgres:admin123@localhost:5432/imovel_gestao

# JWT/Security
SECRET_KEY=sua-secret-key-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
ENVIRONMENT=development
DEBUG=true
PROJECT_NAME=Imóvel Gestão API
VERSION=1.0.0
API_V1_STR=/api/v1

# Server
HOST=0.0.0.0
PORT=8000

# Upload
UPLOAD_DIR=./uploads
```

### 5. Executar com Docker (Recomendado)

```bash
# Subir banco de dados e aplicação
docker-compose up --build

# Ou apenas o banco (e rodar app localmente)
docker-compose up postgres
```

### 6. Executar Localmente (sem Docker)

```bash
# Certifique-se de ter PostgreSQL rodando
# Execute as migrations (se necessário)
# Inicie o servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Acessar a Aplicação

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

---

## 🧪 Executar Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=app --cov-report=html

# Ver relatório de coverage
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
xdg-open htmlcov/index.html  # Linux
```

---

## 🔧 Comandos Úteis

### Usando Make (Windows/Linux/Mac)

```bash
# Instalar dependências
make install

# Executar testes
make test

# Executar linting
make lint

# Formatar código
make format

# Executar servidor
make run

# Limpar cache
make clean
```

### Manualmente

```bash
# Formatar código
black app tests
isort app tests

# Verificar estilo
flake8 app tests

# Type checking
mypy app
```

---

## 📁 Estrutura do Projeto

```
Backend/
├── app/
│   ├── api/v1/          # Rotas da API
│   ├── core/            # Configurações e utilitários
│   ├── db/              # Banco de dados e modelos
│   └── src/             # Módulos de domínio
│       ├── properties/  # Propriedades
│       ├── tenants/     # Inquilinos
│       ├── contracts/   # Contratos
│       ├── payments/    # Pagamentos
│       ├── expenses/    # Despesas
│       └── notifications/ # Notificações
├── tests/               # Testes automatizados
├── docker-compose.yml   # Configuração Docker
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

---

## 🔐 Autenticação

O backend usa JWT tokens gerado pelo **Auth-API** separado.

### Como Autenticar:

1. **Fazer login no Auth-API:**
```bash
POST https://auth-api-3zxk.onrender.com/api/v1/auth/login
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

2. **Usar o token nas requisições:**
```bash
Authorization: Bearer <seu_token>
```

3. **Testar no Swagger:**
- Acesse http://localhost:8000/api/v1/docs
- Clique em **Authorize**
- Cole o token
- Teste os endpoints protegidos

---

## 🌍 CORS

O backend está configurado para aceitar requisições de:

- `http://localhost:3000` (Next.js dev)
- `http://localhost:3001` (React dev)
- `http://localhost:5173` (Vite dev)
- `https://imobly.onrender.com` (Frontend em produção)
- `https://auth-api-3zxk.onrender.com` (Auth-API)

Para adicionar novas origens, edite `app/core/config.py`:

```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    # Adicione aqui...
]
```

---

## 📚 Documentação Completa

Para documentação detalhada sobre:
- Arquitetura do sistema
- Guias de API
- Exemplos de uso
- Diagramas
- Deploy e CI/CD

**Acesse:** https://imobly.github.io/Documentation/

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

**Importante:** Todos os PRs devem passar nos testes e linters do CI/CD.

---

## 📄 Licença

Este projeto é privado e pertence à Imobly.

---

## 📞 Suporte

- **Issues**: https://github.com/Imobly/Backend/issues
- **Documentação**: https://imobly.github.io/Documentation/

---

**Desenvolvido com ❤️ pela equipe Imobly**
