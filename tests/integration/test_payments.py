"""Integration tests for Payments API"""

from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestPaymentsAPI:
    """Test Payments CRUD endpoints"""

    def test_create_payment(
        self,
        client: TestClient,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
        sample_payment_data,
    ):
        """Test creating a payment"""
        # Create property
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]

        # Create tenant
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]

        # Create contract
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        contract_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = contract_response.json()["id"]

        # Create payment
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_id
        payment_data["tenant_id"] = tenant_id
        payment_data["contract_id"] = contract_id
        payment_data["due_date"] = payment_data["due_date"].isoformat()

        response = client.post("/api/v1/payments/", json=payment_data)
        assert response.status_code == 201
        
        payment = response.json()
        assert payment["status"] == "pending"
        assert "id" in payment

    def test_get_payment(self, client: TestClient, sample_property_data, sample_tenant_data, sample_contract_data, sample_payment_data):
        """Test retrieving a payment by ID"""
        # Create dependencies
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        contract_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = contract_response.json()["id"]

        # Create payment
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_id
        payment_data["tenant_id"] = tenant_id
        payment_data["contract_id"] = contract_id
        payment_data["due_date"] = payment_data["due_date"].isoformat()
        create_response = client.post("/api/v1/payments/", json=payment_data)
        payment_id = create_response.json()["id"]

        # Get payment
        response = client.get(f"/api/v1/payments/{payment_id}")
        assert response.status_code == 200
        assert response.json()["id"] == payment_id

    def test_list_payments(self, client: TestClient):
        """Test listing payments"""
        response = client.get("/api/v1/payments/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_payment(self, client: TestClient, sample_property_data, sample_tenant_data, sample_contract_data, sample_payment_data):
        """Test updating a payment"""
        # Create dependencies
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        contract_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = contract_response.json()["id"]

        # Create payment
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_id
        payment_data["tenant_id"] = tenant_id
        payment_data["contract_id"] = contract_id
        payment_data["due_date"] = payment_data["due_date"].isoformat()
        create_response = client.post("/api/v1/payments/", json=payment_data)
        payment_id = create_response.json()["id"]

        # Update to paid
        update_data = {
            "status": "paid",
            "payment_date": "2025-01-03",
            "payment_method": "pix"
        }
        response = client.put(f"/api/v1/payments/{payment_id}", json=update_data)
        assert response.status_code == 200
        
        updated = response.json()
        assert updated["status"] == "paid"
        assert updated["payment_method"] == "pix"

    def test_delete_payment(self, client: TestClient, sample_property_data, sample_tenant_data, sample_contract_data, sample_payment_data):
        """Test deleting a payment"""
        # Create dependencies
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]
        tenant_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = tenant_response.json()["id"]
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id
        contract_data["start_date"] = contract_data["start_date"].isoformat()
        contract_data["end_date"] = contract_data["end_date"].isoformat()
        contract_response = client.post("/api/v1/contracts/", json=contract_data)
        contract_id = contract_response.json()["id"]

        # Create payment
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_id
        payment_data["tenant_id"] = tenant_id
        payment_data["contract_id"] = contract_id
        payment_data["due_date"] = payment_data["due_date"].isoformat()
        create_response = client.post("/api/v1/payments/", json=payment_data)
        payment_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/payments/{payment_id}")
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f"/api/v1/payments/{payment_id}")
        assert get_response.status_code == 404
