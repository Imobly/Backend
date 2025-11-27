"""Integration tests for Expenses API"""

from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestExpensesAPI:
    """Test Expenses CRUD endpoints"""

    def test_create_expense(self, client: TestClient, sample_property_data, sample_expense_data):
        """Test creating an expense"""
        # Create property
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]

        # Create expense
        expense_data = sample_expense_data.copy()
        expense_data["property_id"] = property_id
        expense_data["date"] = expense_data["date"].isoformat()

        response = client.post("/api/v1/expenses/", json=expense_data)
        assert response.status_code == 201

        expense = response.json()
        assert expense["description"] == sample_expense_data["description"]
        assert expense["status"] == "pending"
        assert "id" in expense

    def test_get_expense(self, client: TestClient, sample_property_data, sample_expense_data):
        """Test retrieving an expense by ID"""
        # Create property
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]

        # Create expense
        expense_data = sample_expense_data.copy()
        expense_data["property_id"] = property_id
        expense_data["date"] = expense_data["date"].isoformat()
        create_response = client.post("/api/v1/expenses/", json=expense_data)
        expense_id = create_response.json()["id"]

        # Get expense
        response = client.get(f"/api/v1/expenses/{expense_id}")
        assert response.status_code == 200
        assert response.json()["id"] == expense_id

    def test_list_expenses(self, client: TestClient):
        """Test listing expenses"""
        response = client.get("/api/v1/expenses/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_expense(self, client: TestClient, sample_property_data, sample_expense_data):
        """Test updating an expense"""
        # Create property
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]

        # Create expense
        expense_data = sample_expense_data.copy()
        expense_data["property_id"] = property_id
        expense_data["date"] = expense_data["date"].isoformat()
        create_response = client.post("/api/v1/expenses/", json=expense_data)
        expense_id = create_response.json()["id"]

        # Update
        update_data = {"status": "paid", "amount": 300.00}
        response = client.put(f"/api/v1/expenses/{expense_id}", json=update_data)
        assert response.status_code == 200

        updated = response.json()
        assert updated["status"] == "paid"
        assert float(updated["amount"]) == 300.00

    def test_delete_expense(self, client: TestClient, sample_property_data, sample_expense_data):
        """Test deleting an expense"""
        # Create property
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]

        # Create expense
        expense_data = sample_expense_data.copy()
        expense_data["property_id"] = property_id
        expense_data["date"] = expense_data["date"].isoformat()
        create_response = client.post("/api/v1/expenses/", json=expense_data)
        expense_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/expenses/{expense_id}")
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f"/api/v1/expenses/{expense_id}")
        assert get_response.status_code == 404

    def test_list_expenses_by_property(
        self, client: TestClient, sample_property_data, sample_expense_data
    ):
        """Test listing expenses filtered by property"""
        # Create property
        prop_response = client.post("/api/v1/properties/", json=sample_property_data)
        property_id = prop_response.json()["id"]

        # Create expense
        expense_data = sample_expense_data.copy()
        expense_data["property_id"] = property_id
        expense_data["date"] = expense_data["date"].isoformat()
        client.post("/api/v1/expenses/", json=expense_data)

        # List by property
        response = client.get(f"/api/v1/expenses/?property_id={property_id}")
        assert response.status_code == 200
        expenses = response.json()
        assert len(expenses) > 0
        assert all(exp["property_id"] == property_id for exp in expenses)
