"""Integration tests for Tenants API"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestTenantsAPI:
    """Test Tenants CRUD endpoints"""

    def test_create_tenant(self, client: TestClient, sample_tenant_data):
        """Test creating a tenant"""
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code == 201

        tenant = response.json()
        assert tenant["name"] == sample_tenant_data["name"]
        assert tenant["email"] == sample_tenant_data["email"]
        assert "id" in tenant

    def test_get_tenant(self, client: TestClient, sample_tenant_data):
        """Test retrieving a tenant by ID"""
        # Create tenant
        create_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = create_response.json()["id"]

        # Get tenant
        response = client.get(f"/api/v1/tenants/{tenant_id}")
        assert response.status_code == 200
        assert response.json()["id"] == tenant_id

    def test_list_tenants(self, client: TestClient):
        """Test listing tenants"""
        response = client.get("/api/v1/tenants/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_tenant(self, client: TestClient, sample_tenant_data):
        """Test updating a tenant"""
        # Create tenant
        create_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = create_response.json()["id"]

        # Update
        update_data = {"phone": "+5511888888888", "profession": "Developer"}
        response = client.put(f"/api/v1/tenants/{tenant_id}", json=update_data)
        assert response.status_code == 200

        updated = response.json()
        assert updated["phone"] == "+5511888888888"
        assert updated["profession"] == "Developer"

    def test_delete_tenant(self, client: TestClient, sample_tenant_data):
        """Test deleting a tenant"""
        # Create tenant
        create_response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        tenant_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/tenants/{tenant_id}")
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f"/api/v1/tenants/{tenant_id}")
        assert get_response.status_code == 404

    def test_tenant_email_uniqueness(self, client: TestClient, sample_tenant_data):
        """Test that tenant email must be unique"""
        # Create first tenant
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code == 201

        # Try to create another with same email
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code in [400, 422]

    def test_tenant_cpf_uniqueness(self, client: TestClient, sample_tenant_data):
        """Test that tenant CPF must be unique"""
        # Create first tenant
        response = client.post("/api/v1/tenants/", json=sample_tenant_data)
        assert response.status_code == 201

        # Try to create another with same CPF but different email
        data = sample_tenant_data.copy()
        data["email"] = "different@example.com"
        response = client.post("/api/v1/tenants/", json=data)
        assert response.status_code in [400, 422]
