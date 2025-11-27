"""Integration tests for Contracts API"""

from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestContractsAPI:
    """Test Contracts CRUD endpoints"""

    def test_create_contract(
        self,
        client: TestClient,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
    ):
        """Test creating a contract"""
        # Create property first
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        assert prop_response.status_code == 201
        property_id = prop_response.json()["id"]

        # Create tenant
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert tenant_response.status_code == 201
        tenant_id = tenant_response.json()["id"]

        # Create contract
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()

        response = client.post("/api/v1/contracts/", json=contract_data)
        assert response.status_code == 201

        contract = response.json()
        assert contract["property_id"] == property_id
        assert contract["tenant_id"] == tenant_id
        assert contract["status"] == "active"

    def test_get_contract(
        self,
        client: TestClient,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
    ):
        """Test retrieving a contract by ID"""
        # Create dependencies
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]

        # Create contract
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        create_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = create_response.json()["id"]

        # Get contract
        response = client.get(f"/api/v1/contracts/{contract_id}")
        assert response.status_code == 200
        assert response.json()["id"] == contract_id

    def test_list_contracts(self, client: TestClient):
        """Test listing contracts"""
        response = client.get("/api/v1/contracts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_contract(
        self, client: TestClient, sample_property_data, sample_tenant_data, sample_contract_data
    ):
        """Test updating a contract"""
        # Create dependencies
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]

        # Create contract
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        create_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = create_response.json()["id"]

        # Update
        update_data = {"rent": 2000.00}
        response = client.put(f"/api/v1/contracts/{contract_id}", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert float(updated["rent"]) == 2000.00

    def test_delete_contract(
        self, client: TestClient, sample_property_data, sample_tenant_data, sample_contract_data
    ):
        """Test deleting a contract"""
        # Create dependencies
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]

        # Create contract
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        create_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/contracts/{contract_id}")
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f"/api/v1/contracts/{contract_id}")
        assert get_response.status_code == 404
