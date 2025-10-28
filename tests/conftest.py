"""Pytest configuration and fixtures"""

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.src.auth.repository import UserRepository
from app.src.auth.schemas import UserCreate

# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with the test database"""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_property_data():
    """Sample property data for tests"""
    return {
        "name": "Test Property",
        "address": "Test Address, 123",
        "neighborhood": "Test Neighborhood",
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345-678",
        "type": "apartment",
        "area": 80.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "parking_spaces": 1,
        "rent": 1500.00,
        "status": "vacant",
        "description": "Test description",
        "is_residential": True,
    }


@pytest.fixture
def sample_tenant_data():
    """Sample tenant data for tests"""
    return {
        "name": "Test Tenant",
        "email": "test@example.com",
        "phone": "+5511999999999",
        "cpf_cnpj": "12345678901",
        "profession": "Software Engineer",
        "status": "active",
    }


@pytest.fixture
def sample_unit_data():
    """Sample unit data for tests"""
    return {
        "property_id": 1,
        "number": "101",
        "area": 75.5,
        "bedrooms": 2,
        "bathrooms": 1,
        "rent": 1500.00,
        "status": "vacant",
    }


@pytest.fixture
def sample_contract_data():
    """Sample contract data for tests"""
    return {
        "title": "Test Contract",
        "property_id": 1,
        "tenant_id": 1,
        "start_date": "2025-01-01",
        "end_date": "2026-01-01",
        "rent": 1500.00,
        "deposit": 1500.00,
        "interest_rate": 1.0,
        "fine_rate": 2.0,
        "status": "active",
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for tests"""
    return {
        "property_id": 1,
        "tenant_id": 1,
        "contract_id": 1,
        "due_date": "2025-01-05",
        "amount": 1500.00,
        "fine_amount": 0.0,
        "total_amount": 1500.00,
        "status": "pending",
    }


@pytest.fixture
def sample_expense_data():
    """Sample expense data for tests"""
    return {
        "property_id": 1,
        "description": "Test Expense",
        "amount": 250.00,
        "category": "maintenance",
        "due_date": "2025-01-10",
        "status": "pending",
    }


# ============ Authentication Fixtures ============


@pytest.fixture
def sample_user_data():
    """Sample user data for tests"""
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "senha123",
        "full_name": "Test User",
    }


@pytest.fixture
def sample_user(db: Session, sample_user_data):
    """Create a sample user in the database"""
    user_repo = UserRepository()
    user_create = UserCreate(**sample_user_data)
    user = user_repo.create_user(db, user_create)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
    }


@pytest.fixture
def auth_headers(client: TestClient, sample_user):
    """Get authentication headers with valid token"""
    login_data = {"username": sample_user["username"], "password": "senha123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def superuser_data():
    """Sample superuser data for tests"""
    return {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin123",
        "full_name": "Admin User",
    }


@pytest.fixture
def superuser(db: Session, superuser_data):
    """Create a superuser in the database"""
    user_repo = UserRepository()
    user_create = UserCreate(**superuser_data)
    user = user_repo.create_user(db, user_create)

    # Set as superuser
    user.is_superuser = True
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
    }


@pytest.fixture
def superuser_headers(client: TestClient, superuser):
    """Get authentication headers for superuser"""
    login_data = {"username": superuser["username"], "password": "admin123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
