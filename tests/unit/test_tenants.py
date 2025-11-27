"""Unit tests for Tenants module"""

from sqlalchemy.orm import Session

from app.src.tenants.repository import TenantRepository
from app.src.tenants.schemas import TenantCreate, TenantUpdate


class TestTenantRepository:
    """Test Tenant Repository"""

    def test_create_tenant(self, db: Session, sample_tenant_data):
        """Test creating a tenant"""
        repo = TenantRepository(db)
        tenant_create = TenantCreate(**sample_tenant_data)

        tenant_obj = repo.create(db, obj_in=tenant_create)

        assert tenant_obj.id is not None
        assert tenant_obj.name == sample_tenant_data["name"]
        assert tenant_obj.email == sample_tenant_data["email"]
        assert tenant_obj.cpf_cnpj == sample_tenant_data["cpf_cnpj"]

    def test_get_by_email(self, db: Session, sample_tenant_data):
        """Test getting tenant by email"""
        repo = TenantRepository(db)
        tenant_create = TenantCreate(**sample_tenant_data)

        created = repo.create(db, obj_in=tenant_create)
        retrieved = repo.get_by_email(db, user_id=1, email=created.email)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.email == created.email

    def test_get_by_cpf(self, db: Session, sample_tenant_data):
        """Test getting tenant by CPF"""
        repo = TenantRepository(db)
        tenant_create = TenantCreate(**sample_tenant_data)

        created = repo.create(db, obj_in=tenant_create)
        retrieved = repo.get_by_cpf(db, user_id=1, cpf=created.cpf_cnpj)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.cpf_cnpj == created.cpf_cnpj

    def test_check_unique_constraints_email(self, db: Session, sample_tenant_data):
        """Test email uniqueness validation"""
        repo = TenantRepository(db)
        tenant_create = TenantCreate(**sample_tenant_data)

        # Create first tenant
        repo.create(db, obj_in=tenant_create)

        # Try to create with same email
        errors = repo.check_unique_constraints(db, user_id=1, tenant_data=tenant_create)

        assert "email" in errors
        assert "já está em uso" in errors["email"]

    def test_check_unique_constraints_cpf(self, db: Session, sample_tenant_data):
        """Test CPF uniqueness validation"""
        repo = TenantRepository(db)
        tenant_create = TenantCreate(**sample_tenant_data)

        # Create first tenant
        repo.create(db, obj_in=tenant_create)

        # Try to create with same CPF but different email
        data = sample_tenant_data.copy()
        data["email"] = "different@example.com"
        tenant_create_2 = TenantCreate(**data)

        errors = repo.check_unique_constraints(db, user_id=1, tenant_data=tenant_create_2)

        assert "cpf_cnpj" in errors
        assert "já está em uso" in errors["cpf_cnpj"]

    def test_search_tenants_by_name(self, db: Session, sample_tenant_data):
        """Test searching tenants by name"""
        repo = TenantRepository(db)

        # Create tenants with different names
        for i in range(3):
            data = sample_tenant_data.copy()
            data["name"] = f"Tenant {i}"
            data["email"] = f"tenant{i}@example.com"
            data["cpf_cnpj"] = f"1234567890{i}"
            tenant_create = TenantCreate(**data)
            repo.create(db, obj_in=tenant_create)

        # Search
        results = repo.search_tenants(db, user_id=1, name="Tenant 1")

        assert len(results) >= 1
        assert "Tenant 1" in results[0].name

    def test_update_tenant(self, db: Session, sample_tenant_data):
        """Test updating a tenant"""
        repo = TenantRepository(db)
        tenant_create = TenantCreate(**sample_tenant_data)

        created = repo.create(db, obj_in=tenant_create)

        update_data = TenantUpdate(phone="+5511888888888", profession="Developer")
        updated = repo.update(db, db_obj=created, obj_in=update_data)

        assert updated.phone == "+5511888888888"
        assert updated.profession == "Developer"
        assert updated.name == sample_tenant_data["name"]
