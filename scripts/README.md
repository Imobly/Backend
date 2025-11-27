# Scripts de Teste Manual

Este diretório contém scripts PowerShell para **testes manuais exploratórios** da API.

⚠️ **Estes scripts NÃO fazem parte da suite automatizada de testes**

## 🎯 Quando usar estes scripts?

Use estes scripts para:
- ✅ Testar **upload de arquivos** (multipart/form-data)
- ✅ Debug manual de endpoints específicos
- ✅ Exploração/validação rápida de funcionalidades
- ✅ Testes de integração com sistemas externos

## 📋 Scripts Recomendados

### Úteis para Testes Manuais
- ✅ `test_expenses_complete.ps1` - **Fluxo completo de despesas** (CRUD + upload)
- ✅ `test_expense_documents.ps1` - **Upload de documentos de despesas**
- ✅ `test_tenant_upload.ps1` - **Upload de documentos de inquilinos**  
- ✅ `test_endpoints.ps1` - **Framework genérico** para testar qualquer endpoint

### Obsoletos (podem ser removidos)
- ❌ `test_simple.ps1` - Apenas health check (trivial)
- ❌ `test_simple_docs.ps1` - Duplicado
- ❌ `test_api.ps1` - Funcionalidade já coberta por testes automatizados

## 🚀 Como Usar

1. **Inicie o backend**:
   ```powershell
   docker compose up
   ```

2. **Execute o script desejado**:
   ```powershell
   .\test_expenses_complete.ps1
   ```

## 🧪 Testes Automatizados

Para testes automatizados (executados no CI/CD), use a suite em `tests/`:

```bash
# Rodar todos os testes
pytest -v

# Rodar testes de integração
pytest tests/integration/ -v

# Rodar dentro do Docker
docker compose exec backend pytest -v
```

## 📁 Estrutura de Testes

```
tests/
├── integration/         # Testes de integração automatizados (CRUD, fluxos)
│   ├── test_properties.py
│   ├── test_tenants.py
│   ├── test_contracts.py
│   ├── test_payments.py
│   ├── test_expenses.py
│   ├── test_dashboard.py
│   └── test_notifications.py
├── unit/               # Testes unitários
└── parametrized/       # Testes parametrizados

scripts/                # Testes manuais (este diretório)
└── test_*.ps1
```

## 🗑️ Limpeza Recomendada

Se quiser limpar scripts obsoletos:

```powershell
# Remover scripts redundantes
Remove-Item .\test_simple.ps1, .\test_simple_docs.ps1, .\test_api.ps1
```

