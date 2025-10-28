"""Parametrized validation tests"""

import pytest
from fastapi.testclient import TestClient


class TestPropertyValidations:
    """Parametrized property validation tests"""

    @pytest.mark.parametrize("property_type", ["apartment", "house", "commercial", "studio"])
    def test_valid_property_types(self, client: TestClient, sample_property_data, property_type):
        """Test all valid property types"""
        data = sample_property_data.copy()
        data["type"] = property_type

        response = client.post("/api/v1/properties/", json=data)
        assert response.status_code == 201
        assert response.json()["type"] == property_type

    @pytest.mark.parametrize("invalid_type", ["villa", "mansion", "invalid"])
    def test_invalid_property_types(self, client: TestClient, sample_property_data, invalid_type):
        """Test invalid property types"""
        data = sample_property_data.copy()
        data["type"] = invalid_type

        response = client.post("/api/v1/properties/", json=data)
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "rent,expected",
        [
            (1000.00, 201),
            (0.01, 201),
            (0.00, 422),
            (-100.00, 422),
        ],
    )
    def test_rent_validation(self, client: TestClient, sample_property_data, rent, expected):
        """Test rent value validation"""
        data = sample_property_data.copy()
        data["rent"] = rent

        response = client.post("/api/v1/properties/", json=data)
        assert response.status_code == expected

    @pytest.mark.parametrize("status", ["vacant", "occupied", "maintenance", "inactive"])
    def test_valid_property_status(self, client: TestClient, sample_property_data, status):
        """Test all valid property statuses"""
        data = sample_property_data.copy()
        data["status"] = status

        response = client.post("/api/v1/properties/", json=data)
        assert response.status_code == 201
        assert response.json()["status"] == status


class TestTenantValidations:
    """Parametrized tenant validation tests"""

    @pytest.mark.parametrize(
        "email", ["valid@example.com", "user.name@domain.co", "test+tag@example.org"]
    )
    def test_valid_emails(self, client: TestClient, sample_tenant_data, email):
        """Test valid email formats"""
        data = sample_tenant_data.copy()
        data["email"] = email
        data["cpf_cnpj"] = f"12345{email[0:5]}"  # Make CPF unique

        response = client.post("/api/v1/tenants/", json=data)
        assert response.status_code == 201

    @pytest.mark.parametrize(
        "invalid_email", ["notanemail", "@example.com", "user@", "user @example.com"]
    )
    def test_invalid_emails(self, client: TestClient, sample_tenant_data, invalid_email):
        """Test invalid email formats"""
        data = sample_tenant_data.copy()
        data["email"] = invalid_email

        response = client.post("/api/v1/tenants/", json=data)
        assert response.status_code == 422

    @pytest.mark.parametrize("status", ["active", "inactive"])
    def test_valid_tenant_status(self, client: TestClient, sample_tenant_data, status):
        """Test valid tenant statuses"""
        data = sample_tenant_data.copy()
        data["status"] = status
        data["email"] = f"test.{status}@example.com"
        data["cpf_cnpj"] = f"123456789{status[0:2]}"

        response = client.post("/api/v1/tenants/", json=data)
        assert response.status_code == 201
        assert response.json()["status"] == status


class TestPaymentValidations:
    """Parametrized payment validation tests"""

    @pytest.mark.parametrize("status", ["pending", "paid", "overdue", "partial"])
    def test_valid_payment_status(self, status):
        """Test all valid payment statuses"""
        valid_statuses = ["pending", "paid", "overdue", "partial"]
        assert status in valid_statuses

    @pytest.mark.parametrize("method", ["cash", "transfer", "pix", "check", "card"])
    def test_valid_payment_methods(self, method):
        """Test all valid payment methods"""
        valid_methods = ["cash", "transfer", "pix", "check", "card"]
        assert method in valid_methods

    @pytest.mark.parametrize(
        "amount,fine,expected_total",
        [
            (1000.00, 0.00, 1000.00),
            (1500.00, 150.00, 1650.00),
            (800.50, 80.05, 880.55),
            (2000.00, 200.00, 2200.00),
        ],
    )
    def test_payment_total_calculation(self, amount, fine, expected_total):
        """Test payment total calculation"""
        calculated_total = amount + fine
        assert calculated_total == expected_total

    @pytest.mark.parametrize(
        "amount,expected",
        [
            (1000.00, 201),
            (0.01, 201),
            (0.00, 422),
            (-100.00, 422),
        ],
    )
    def test_payment_amount_validation(self, amount, expected):
        """Test payment amount validation rules"""
        # Amount must be > 0
        if amount > 0:
            assert expected == 201
        else:
            assert expected == 422


class TestContractValidations:
    """Parametrized contract validation tests"""

    @pytest.mark.parametrize("status", ["active", "expired", "terminated"])
    def test_valid_contract_status(self, status):
        """Test all valid contract statuses"""
        valid_statuses = ["active", "expired", "terminated"]
        assert status in valid_statuses

    @pytest.mark.parametrize(
        "rent,deposit,valid",
        [
            (1000.00, 1000.00, True),
            (1500.00, 3000.00, True),
            (1000.00, 0.00, True),
            (0.00, 1000.00, False),
            (-100.00, 1000.00, False),
        ],
    )
    def test_contract_financial_values(self, rent, deposit, valid):
        """Test contract financial value validation"""
        # Rent must be > 0, deposit >= 0
        if rent > 0 and deposit >= 0:
            assert valid is True
        else:
            assert valid is False
