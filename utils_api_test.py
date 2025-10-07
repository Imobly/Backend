#!/usr/bin/env python3
"""
🧪 Script de Teste Completo da API Imóvel Gestão
Este script testa todos os endpoints, CRUD operations e funcionalidades.
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, Any
import sys

# Configuração da API
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}

class APITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200, description: str = ""):
        """Testa um endpoint específico"""
        url = f"{BASE_URL}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=HEADERS)
            elif method.upper() == "POST":
                response = requests.post(url, headers=HEADERS, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=HEADERS, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=HEADERS)
            
            if response.status_code == expected_status:
                print(f"✅ {method} {endpoint} - {description}")
                self.passed += 1
                self.results.append({
                    "status": "PASS",
                    "method": method,
                    "endpoint": endpoint,
                    "description": description,
                    "response_code": response.status_code,
                    "response_data": response.json() if response.content else None
                })
                return response.json() if response.content else None
            else:
                print(f"❌ {method} {endpoint} - {description}")
                print(f"   Esperado: {expected_status}, Recebido: {response.status_code}")
                print(f"   Resposta: {response.text}")
                self.failed += 1
                self.results.append({
                    "status": "FAIL",
                    "method": method,
                    "endpoint": endpoint,
                    "description": description,
                    "expected_code": expected_status,
                    "response_code": response.status_code,
                    "error": response.text
                })
                return None
                
        except Exception as e:
            print(f"❌ {method} {endpoint} - ERRO: {str(e)}")
            self.failed += 1
            self.results.append({
                "status": "ERROR",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "error": str(e)
            })
            return None

    def test_properties(self):
        """Testa todos os endpoints de propriedades"""
        print("\n🏠 TESTANDO PROPERTIES ENDPOINTS")
        print("=" * 50)
        
        # 1. Listar propriedades (inicialmente vazio)
        properties = self.test_endpoint("GET", "/properties/", description="Listar propriedades")
        
        # 2. Criar uma propriedade
        property_data = {
            "name": "Casa Teste API",
            "address": "Rua das Flores, 123",
            "neighborhood": "Centro",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01234-567",
            "type": "house",
            "area": "120.5",
            "bedrooms": 3,
            "bathrooms": 2,
            "parking_spaces": 2,
            "rent": "2500.00",
            "status": "vacant",
            "description": "Casa ampla com quintal",
            "images": ["https://example.com/image1.jpg"],
            "is_residential": True,
            "tenant": None
        }
        
        new_property = self.test_endpoint("POST", "/properties/", 
                                        data=property_data, 
                                        expected_status=201,
                                        description="Criar propriedade")
        
        if new_property:
            property_id = new_property.get("id")
            
            # 3. Buscar propriedade por ID
            self.test_endpoint("GET", f"/properties/{property_id}", 
                             description=f"Buscar propriedade ID {property_id}")
            
            # 4. Atualizar propriedade
            update_data = {
                "name": "Casa Teste API - Atualizada",
                "rent": "2800.00",
                "status": "occupied"
            }
            self.test_endpoint("PUT", f"/properties/{property_id}", 
                             data=update_data,
                             description=f"Atualizar propriedade ID {property_id}")
            
            # 5. Listar propriedades novamente (deve ter 1)
            self.test_endpoint("GET", "/properties/", description="Listar propriedades após criação")
            
            # 6. Filtros
            self.test_endpoint("GET", "/properties/?property_type=house", 
                             description="Filtrar por tipo 'house'")
            self.test_endpoint("GET", "/properties/?status=occupied", 
                             description="Filtrar por status 'occupied'")
            self.test_endpoint("GET", "/properties/?min_rent=2000&max_rent=3000", 
                             description="Filtrar por faixa de aluguel")

    def test_tenants(self):
        """Testa todos os endpoints de inquilinos"""
        print("\n👥 TESTANDO TENANTS ENDPOINTS")
        print("=" * 50)
        
        # 1. Listar inquilinos
        tenants = self.test_endpoint("GET", "/tenants/", description="Listar inquilinos")
        
        # 2. Criar inquilino
        import random
        rand_id = random.randint(1000, 9999)
        tenant_data = {
            "name": f"João Silva {rand_id}",
            "email": f"joao.silva.{rand_id}@email.com",
            "phone": "(11) 99999-9999",
            "cpf_cnpj": f"1234567890{rand_id}",
            "birth_date": "1990-05-15",
            "profession": "Engenheiro",
            "emergency_contact": {
                "name": "Maria Silva",
                "phone": "(11) 88888-8888",
                "relationship": "Mãe"
            },
            "documents": [
                {
                    "id": "1",
                    "name": "RG",
                    "type": "identity",
                    "url": "https://example.com/rg.pdf"
                },
                {
                    "id": "2", 
                    "name": "CPF",
                    "type": "identity",
                    "url": "https://example.com/cpf.pdf"
                }
            ],
            "status": "active"
        }
        
        new_tenant = self.test_endpoint("POST", "/tenants/", 
                                      data=tenant_data, 
                                      expected_status=201,
                                      description="Criar inquilino")
        
        if new_tenant:
            tenant_id = new_tenant.get("id")
            
            # 3. Buscar inquilino por ID
            self.test_endpoint("GET", f"/tenants/{tenant_id}", 
                             description=f"Buscar inquilino ID {tenant_id}")
            
            # 4. Atualizar inquilino
            update_data = {
                "name": "João Silva Santos",
                "profession": "Engenheiro Sênior"
            }
            self.test_endpoint("PUT", f"/tenants/{tenant_id}", 
                             data=update_data,
                             description=f"Atualizar inquilino ID {tenant_id}")

    def test_contracts(self):
        """Testa endpoints de contratos"""
        print("\n📄 TESTANDO CONTRACTS ENDPOINTS")
        print("=" * 50)
        
        # Listar contratos
        self.test_endpoint("GET", "/contracts/", description="Listar contratos")
        
        # Criar contrato (precisa de property_id e tenant_id reais)
        from datetime import datetime, timedelta
        start_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=395)).strftime("%Y-%m-%d")
        
        contract_data = {
            "title": f"Contrato Teste {datetime.now().strftime('%Y%m%d%H%M%S')}",
            "property_id": 1,  # Assumindo que existe
            "tenant_id": 1,    # Assumindo que existe  
            "start_date": start_date,
            "end_date": end_date,
            "rent": "2500.00",
            "deposit": "5000.00",
            "interest_rate": "1.5",
            "fine_rate": "2.0",
            "status": "active"
        }
        
        new_contract = self.test_endpoint("POST", "/contracts/", 
                                        data=contract_data, 
                                        expected_status=201,
                                        description="Criar contrato")

    def test_payments(self):
        """Testa endpoints de pagamentos"""
        print("\n💰 TESTANDO PAYMENTS ENDPOINTS")
        print("=" * 50)
        
        # Listar pagamentos
        self.test_endpoint("GET", "/payments/", description="Listar pagamentos")
        
        # Criar pagamento
        payment_data = {
            "property_id": 1,
            "tenant_id": 1,
            "contract_id": 2,  # ID do contrato existente
            "due_date": "2024-01-05",
            "amount": "2500.00",
            "total_amount": "2500.00",
            "status": "pending",
            "description": "Aluguel Janeiro 2024"
        }
        
        self.test_endpoint("POST", "/payments/", 
                         data=payment_data, 
                         expected_status=201,
                         description="Criar pagamento")

    def test_expenses(self):
        """Testa endpoints de despesas"""
        print("\n💸 TESTANDO EXPENSES ENDPOINTS")
        print("=" * 50)
        
        # Listar despesas
        self.test_endpoint("GET", "/expenses/", description="Listar despesas")
        
        # Criar despesa
        expense_data = {
            "type": "maintenance",
            "category": "Reparo",
            "description": "Conserto da torneira",
            "amount": "150.00",
            "date": "2024-01-10",
            "property_id": 1,
            "status": "paid",
            "vendor": "Encanador João",
            "notes": "Reparo emergencial"
        }
        
        self.test_endpoint("POST", "/expenses/", 
                         data=expense_data, 
                         expected_status=201,
                         description="Criar despesa")

    def test_notifications(self):
        """Testa endpoints de notificações"""
        print("\n🔔 TESTANDO NOTIFICATIONS ENDPOINTS")
        print("=" * 50)
        
        # Listar notificações
        self.test_endpoint("GET", "/notifications/", description="Listar notificações")
        
        # Criar notificação
        notification_data = {
            "type": "payment_overdue",
            "title": "Pagamento em Atraso",
            "message": "O pagamento do inquilino João está atrasado",
            "date": datetime.now().isoformat(),
            "priority": "high",
            "read_status": False,
            "action_required": True,
            "related_id": "1",
            "related_type": "payment"
        }
        
        self.test_endpoint("POST", "/notifications/", 
                         data=notification_data, 
                         expected_status=201,
                         description="Criar notificação")

    def test_units(self):
        """Testa endpoints de unidades"""
        print("\n🏢 TESTANDO UNITS ENDPOINTS")
        print("=" * 50)
        
        # Listar unidades
        self.test_endpoint("GET", "/units/", description="Listar unidades")
        
        # Criar unidade
        unit_data = {
            "property_id": 1,
            "number": "101",
            "area": "65.0",
            "bedrooms": 2,
            "bathrooms": 1,
            "rent": "1800.00",
            "status": "vacant",
            "tenant": None
        }
        
        self.test_endpoint("POST", "/units/", 
                         data=unit_data, 
                         expected_status=201,
                         description="Criar unidade")

    def test_dashboard(self):
        """Testa endpoints do dashboard"""
        print("\n📊 TESTANDO DASHBOARD ENDPOINTS")
        print("=" * 50)
        
        # Estatísticas do dashboard
        self.test_endpoint("GET", "/dashboard/stats", description="Estatísticas do dashboard")

    def run_all_tests(self):
        """Executa todos os testes"""
        print("🧪 INICIANDO TESTES COMPLETOS DA API")
        print("=" * 60)
        
        # Verificar se API está respondendo
        try:
            response = requests.get(f"{BASE_URL}/properties/", headers=HEADERS, timeout=5)
            print(f"✅ API está respondendo (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ API não está respondendo: {e}")
            return
        
        # Executar todos os testes
        self.test_properties()
        self.test_tenants()
        self.test_contracts()
        self.test_payments()
        self.test_expenses()
        self.test_notifications()
        self.test_units()
        self.test_dashboard()
        
        # Relatório final
        print("\n" + "=" * 60)
        print("📋 RELATÓRIO FINAL DOS TESTES")
        print("=" * 60)
        print(f"✅ Testes Passaram: {self.passed}")
        print(f"❌ Testes Falharam: {self.failed}")
        print(f"📊 Total de Testes: {self.passed + self.failed}")
        
        if self.failed > 0:
            print(f"\n⚠️ {self.failed} testes falharam. Verifique os erros acima.")
        else:
            print("\n🎉 Todos os testes passaram! Sua API está funcionando perfeitamente!")
        
        # Salvar relatório detalhado
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n📄 Relatório detalhado salvo em: test_results.json")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()