# Imóvel Gestão - Backend API

Este é o backend da aplicação de gestão de imóveis, desenvolvido com FastAPI e organizado para funcionar de forma independente do frontend.

## 🚀 Como executar

### Opção 1: Com Docker (Recomendado)

1. **Copie o arquivo de configuração:**
   ```bash
   cp .env.example .env
   ```

2. **Execute com Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   Isso irá:
   - Configurar o banco MySQL automaticamente
   - Instalar todas as dependências
   - Executar a API na porta 8000
   - Configurar auto-reload para desenvolvimento

### Opção 2: Executar localmente

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure o banco de dados no arquivo .env**

3. **Execute a aplicação:**
   ```bash
   python main.py
   ```

## 📡 API Endpoints

A API estará disponível em: `http://localhost:8000`

### Documentação automática:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Principais endpoints:

#### Propriedades
- `GET /api/v1/properties` - Listar propriedades
- `POST /api/v1/properties` - Criar propriedade
- `GET /api/v1/properties/{id}` - Obter propriedade
- `PUT /api/v1/properties/{id}` - Atualizar propriedade
- `DELETE /api/v1/properties/{id}` - Deletar propriedade

#### Inquilinos
- `GET /api/v1/tenants` - Listar inquilinos
- `POST /api/v1/tenants` - Criar inquilino
- `GET /api/v1/tenants/{id}` - Obter inquilino
- `PUT /api/v1/tenants/{id}` - Atualizar inquilino
- `DELETE /api/v1/tenants/{id}` - Deletar inquilino

## 🔧 Configuração

### Variáveis de ambiente (.env)

```env
# Banco de dados
DATABASE_URL=mysql+pymysql://root:admin123@localhost:3306/imovel_gestao

# Segurança
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Servidor
DEBUG=true
HOST=0.0.0.0
PORT=8000

# URLs do frontend permitidas
FRONTEND_URLS=http://localhost:3000,http://127.0.0.1:3000
```

## 🌐 CORS e Comunicação com Frontend

O backend está configurado para permitir requisições do frontend em:
- `http://localhost:3000` (Next.js padrão)
- `http://127.0.0.1:3000`
- `http://localhost:3001`

Para adicionar novas URLs, modifique a configuração em `app/core/config.py` ou use a variável de ambiente `FRONTEND_URLS`.

## 🗄️ Banco de Dados

### Com Docker
O docker-compose.yml já configura um MySQL automático.

### Manual
1. Instale MySQL
2. Crie o banco: `CREATE DATABASE imovel_gestao;`
3. Configure a URL no .env

## 🔄 Desenvolvimento

### Estrutura de desenvolvimento:
1. **Models** (`app/models/`) - Definições das tabelas
2. **Schemas** (`app/schemas/`) - Validação de dados
3. **Services** (`app/services/`) - Lógica de negócio
4. **Endpoints** (`app/api/v1/endpoints/`) - Rotas da API


## 🤝 Integração com Frontend

O backend está preparado para funcionar com qualquer frontend que consuma APIs REST. As principais características:

- **CORS configurado** para desenvolvimento e produção
- **Documentação automática** com Swagger
- **Versionamento da API** (`/api/v1/`)
- **Padrões RESTful** consistentes
- **Validação de dados** com Pydantic
- **Tratamento de erros** padronizado