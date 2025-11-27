"""Integration tests for Properties API"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestPropertiesAPI:
    """Test Properties CRUD endpoints"""

    def test_create_property(self, client: TestClient, sample_property_data):
        """Test creating a property"""
        response = client.post("/api/v1/properties/", json=sample_property_data)
        assert response.status_code == 201

        property_obj = response.json()
        assert property_obj["name"] == sample_property_data["name"]
        assert property_obj["status"] == "vacant"
        assert "id" in property_obj

    def test_get_property(self, client: TestClient, sample_property_data):
        """Test retrieving a property by ID"""
        # Create property
        create_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = create_response.json()["id"]

        # Get property
        response = client.get(f"/api/v1/properties/{property_id}")
        assert response.status_code == 200
        assert response.json()["id"] == property_id

    def test_list_properties(self, client: TestClient):
        """Test listing properties"""
        response = client.get("/api/v1/properties/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_properties_with_filters(self, client: TestClient, sample_property_data):
        """Test listing properties with filters"""
        # Create property
        client.post("/api/v1/properties/", json=sample_property_data)

        # Filter by type
        response = client.get("/api/v1/properties/?property_type=apartment")
        assert response.status_code == 200

        # Filter by status
        response = client.get("/api/v1/properties/?status=vacant")
        assert response.status_code == 200

    def test_update_property(self, client: TestClient, sample_property_data):
        """Test updating a property"""
        # Create property
        create_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = create_response.json()["id"]

        # Update
        update_data = {"status": "occupied", "rent": 2000.00}
        response = client.put(f"/api/v1/properties/{property_id}", json=update_data)
        assert response.status_code == 200

        updated = response.json()
        assert updated["status"] == "occupied"
        assert float(updated["rent"]) == 2000.00

    def test_update_property_status(self, client: TestClient, sample_property_data):
        """Test updating property status via PATCH endpoint"""
        # Create property
        create_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = create_response.json()["id"]

        # Update status
        response = client.patch(f"/api/v1/properties/{property_id}/status?status=occupied")
        assert response.status_code == 200
        assert response.json()["status"] == "occupied"

    def test_delete_property(self, client: TestClient, sample_property_data):
        """Test deleting a property"""
        # Create property
        create_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/properties/{property_id}")
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f"/api/v1/properties/{property_id}")
        assert get_response.status_code == 404

    def test_get_available_properties(self, client: TestClient, sample_property_data):
        """Test getting only available (vacant) properties"""
        response = client.get("/api/v1/properties/available")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
