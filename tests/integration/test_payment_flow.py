"""Integration tests for complete payment flow"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestPaymentFlow:
    """Test complete payment workflow"""

    def test_complete_payment_flow(
        self,
        client: TestClient,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
        sample_payment_data,
    ):
        """Test creating property -> tenant -> contract -> payment"""

        # 1. Create property
        response = client.post("/api/v1/properties/", json=sample_property_data)
        assert response.status_code == 201
        property_id = response.json()["id"]

        # 2. Create tenant
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code == 201
        tenant_id = response.json()["id"]

        # 3. Create contract
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_id
        contract_data["tenant_id"] = tenant_id

        response = client.post("/api/v1/contracts/", json=contract_data)
        assert response.status_code == 201
        contract_id = response.json()["id"]

        # 4. Create payment
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_id
        payment_data["tenant_id"] = tenant_id
        payment_data["contract_id"] = contract_id

        response = client.post("/api/v1/payments/", json=payment_data)
        assert response.status_code == 201
        payment = response.json()

        assert payment["property_id"] == property_id
        assert payment["tenant_id"] == tenant_id
        assert payment["contract_id"] == contract_id
        assert payment["status"] == "pending"

        # 5. Update payment to paid
        payment_id = payment["id"]
        update_data = {"status": "paid", "payment_date": "2025-01-03", "payment_method": "pix"}

        response = client.put(f"/api/v1/payments/{payment_id}", json=update_data)
        assert response.status_code == 200

        updated_payment = response.json()
        assert updated_payment["status"] == "paid"
        assert updated_payment["payment_method"] == "pix"

        # 6. Verify payment list
        response = client.get(f"/api/v1/payments/?tenant_id={tenant_id}")
        assert response.status_code == 200

        payments = response.json()
        assert len(payments) > 0
        assert payments[0]["id"] == payment_id

    def test_payment_requires_valid_contract(self, client: TestClient, sample_payment_data):
        """Test that payment creation requires valid contract"""
        payment_data = sample_payment_data.copy()
        payment_data["contract_id"] = 99999  # Non-existent contract

        response = client.post("/api/v1/payments/", json=payment_data)
        # Should fail with 400, 404, or 422
        assert response.status_code in [400, 404, 422]

    def test_tenant_uniqueness_email(self, client: TestClient, sample_tenant_data):
        """Test tenant email uniqueness constraint"""
        # Create first tenant
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code == 201

        # Try to create another with same email
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code in [400, 422]

    def test_tenant_uniqueness_cpf(self, client: TestClient, sample_tenant_data):
        """Test tenant CPF uniqueness constraint"""
        # Create first tenant
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code == 201

        # Try to create another with same CPF but different email
        data = sample_tenant_data.copy()
        data["email"] = "different@example.com"

        response = client.post("/api/v1/tenants/", json=data)
        assert response.status_code in [400, 422]

    def test_property_unit_relationship(
        self, client: TestClient, sample_property_data, sample_unit_data
    ):
        """Test property and unit relationship"""
        # Create property
        response = client.post("/api/v1/properties/", json=sample_property_data)
        assert response.status_code == 201
        property_id = response.json()["id"]

        # Create unit for this property
        unit_data = sample_unit_data.copy()
        unit_data["property_id"] = property_id

        response = client.post("/api/v1/units/", json=unit_data)
        assert response.status_code == 201
        unit = response.json()

        assert unit["property_id"] == property_id

        # List units for property
        response = client.get(f"/api/v1/units/?property_id={property_id}")
        assert response.status_code == 200
        units = response.json()
        assert len(units) > 0
