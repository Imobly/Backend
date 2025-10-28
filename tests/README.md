# 🧪 Test Suite Documentation

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Configurações e fixtures do pytest
├── unit/                    # Testes unitários
│   ├── __init__.py
│   ├── test_properties.py
│   ├── test_tenants.py
│   └── test_payments.py
├── integration/             # Testes de integração
│   ├── __init__.py
│   └── test_payment_flow.py
└── parametrized/           # Testes parametrizados
    ├── __init__.py
    └── test_validations.py
```

## Executar Testes

### Localmente (com ambiente virtual ativo)

```bash
# Instalar dependências
pip install -r requirements-dev.txt

# Todos os testes
pytest

# Com coverage
pytest --cov=app --cov-report=html

# Apenas testes unitários
pytest tests/unit

# Apenas testes de integração
pytest tests/integration

# Testes parametrizados
pytest tests/parametrized

# Com marcadores
pytest -m unit
pytest -m integration
```

### Docker (Recomendado)

```bash
# Windows PowerShell
.\run_tests.ps1

# Linux/Mac
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
docker-compose -f docker-compose.test.yml down
```

### Usando Make

```bash
# Instalar dependências
make install

# Executar testes
make test

# Executar linting
make lint

# Formatar código
make format

# Testes em Docker
make test-docker

# Limpar cache
make clean
```

## Linting e Formatação

### Verificar código

```bash
# Verificar formatação
black --check app tests

# Verificar imports
isort --check app tests

# Verificar estilo
flake8 app tests

# Verificar tipos
mypy app
```

### Formatar código automaticamente

```bash
# Formatar com Black
black app tests

# Organizar imports
isort app tests

# Ou usar o make
make format
```

## Coverage Report

Após executar os testes com coverage, abra o relatório HTML:

```bash
# Windows
start htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Mac
open htmlcov/index.html
```

## Fixtures Disponíveis

- **`db`**: Sessão do banco de dados de teste (SQLite in-memory)
- **`client`**: Cliente de teste FastAPI
- **`sample_property_data`**: Dados de exemplo de propriedade
- **`sample_tenant_data`**: Dados de exemplo de inquilino
- **`sample_unit_data`**: Dados de exemplo de unidade
- **`sample_contract_data`**: Dados de exemplo de contrato
- **`sample_payment_data`**: Dados de exemplo de pagamento
- **`sample_expense_data`**: Dados de exemplo de despesa

## Escrevendo Novos Testes

### Teste Unitário

```python
def test_create_entity(db: Session, sample_property_data):
    # Arrange
    repo = PropertyRepository(db)
    data = PropertyCreate(**sample_property_data)
    
    # Act
    result = repo.create(db, obj_in=data)
    
    # Assert
    assert result.id is not None
    assert result.name == sample_property_data["name"]
```

### Teste de Integração

```python
def test_complete_flow(client: TestClient):
    # Create entities in sequence
    response1 = client.post("/api/v1/properties/", json={...})
    assert response1.status_code == 201
    
    response2 = client.post("/api/v1/tenants/", json={...})
    assert response2.status_code == 201
    
    # Verify relationships
    property_id = response1.json()["id"]
    tenant_id = response2.json()["id"]
    assert property_id is not None
    assert tenant_id is not None
```

### Teste Parametrizado

```python
@pytest.mark.parametrize("value,expected", [
    (1000.00, 201),
    (0.01, 201),
    (0.00, 422),
    (-100.00, 422),
])
def test_validation(client: TestClient, value, expected):
    data = {"amount": value}
    response = client.post("/api/v1/endpoint/", json=data)
    assert response.status_code == expected
```

## CI/CD

O projeto possui GitHub Actions configurado para executar automaticamente:

- ✅ Black (formatação)
- ✅ isort (imports)
- ✅ Flake8 (style guide)
- ✅ MyPy (type checking)
- ✅ Pytest (todos os testes)
- ✅ Coverage report

Os testes rodam automaticamente em:
- Push para `main`, `develop`, `develop_costta`
- Pull requests para `main` e `develop`

## Troubleshooting

### Erro de importação do pytest

```bash
pip install -r requirements-dev.txt
```

### Docker não está rodando

```bash
# Inicie o Docker Desktop (Windows/Mac)
# Ou inicie o daemon (Linux)
sudo systemctl start docker
```

### Testes falhando localmente

```bash
# Limpe o cache
make clean

# Reinstale dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Execute novamente
pytest -v
```

### Problemas com banco de dados

Os testes usam SQLite in-memory, então não há necessidade de configurar banco de dados. 
Cada teste recebe um banco limpo através da fixture `db`.

## Configuração de Qualidade

O projeto está configurado para manter nota 10 em qualidade de código com:

- **Black**: Formatação consistente (line-length: 100)
- **isort**: Imports organizados
- **Flake8**: Style guide enforcement
- **MyPy**: Type checking
- **Pytest**: Coverage > 80%
- **Pre-commit hooks**: Validação automática antes do commit

## Comandos Úteis

```bash
# Ver ajuda do Makefile
make help

# Executar apenas um arquivo de teste
pytest tests/unit/test_properties.py

# Executar apenas um teste específico
pytest tests/unit/test_properties.py::TestPropertyRepository::test_create_property

# Ver output dos prints
pytest -s

# Parar no primeiro erro
pytest -x

# Verbose com detalhes
pytest -vv

# Ver testes mais lentos
pytest --durations=10
```

## Padrão AAA (Arrange-Act-Assert)

Todos os testes seguem o padrão AAA:

```python
def test_example(db: Session):
    # Arrange - Preparar dados
    data = {...}
    
    # Act - Executar ação
    result = action(data)
    
    # Assert - Verificar resultado
    assert result.success is True
```
