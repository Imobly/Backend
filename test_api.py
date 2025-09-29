#!/usr/bin/env python3
"""
Script para testar a criação de propriedades via API
"""

import requests
import json

def test_create_property():
    """Testa a criação de uma propriedade"""
    
    # URL da API
    url = "http://localhost:8000/api/v1/properties/"
    
    # Dados da propriedade
    property_data = {
        "name": "APT 123",
        "address": "Rua do gama, 123, Apt 123",
        "neighborhood": "Centro",
        "city": "Gama",
        "state": "DF",
        "zip_code": "01234-5",
        "type": "apartment",
        "area": "85.5",
        "bedrooms": 2,
        "bathrooms": 1,
        "parking_spaces": 1,
        "rent": "2500.00",
        "status": "vacant",
        "description": "Apartamento moderno com vista para a cidade",
        "images": ["https://example.com/image1.jpg"],
        "is_residential": True,
        "tenant": None
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        print("🏠 Testando criação de propriedade...")
        print(f"📍 URL: {url}")
        print(f"📦 Dados: {json.dumps(property_data, indent=2)}")
        print("=" * 50)
        
        # Fazer a requisição POST
        response = requests.post(url, json=property_data, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print("✅ Propriedade criada com sucesso!")
            print(f"🆔 ID: {result.get('id')}")
            print(f"📊 Resposta completa: {json.dumps(result, indent=2)}")
        else:
            print("❌ Erro ao criar propriedade!")
            print(f"🚨 Detalhes: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão! Verifique se o servidor está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_list_properties():
    """Testa a listagem de propriedades"""
    url = "http://localhost:8000/api/v1/properties/"
    
    try:
        print("\n📋 Testando listagem de propriedades...")
        response = requests.get(url)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            properties = response.json()
            print(f"✅ Encontadas {len(properties)} propriedades")
            for prop in properties:
                print(f"  🏠 {prop.get('name')} - {prop.get('address')}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_create_property()
    test_list_properties()