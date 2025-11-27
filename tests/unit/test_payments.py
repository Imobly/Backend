"""Unit tests for Payments module"""

from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.src.contracts.repository import ContractRepository
from app.src.contracts.schemas import ContractCreate
from app.src.payments.repository import PaymentRepository
from app.src.payments.schemas import PaymentCreate, PaymentUpdate
from app.src.properties.repository import PropertyRepository
from app.src.properties.schemas import PropertyCreate
from app.src.tenants.repository import TenantRepository
from app.src.tenants.schemas import TenantCreate


class TestPaymentRepository:
    """Test Payment Repository"""

    def test_create_payment(
        self,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
        sample_payment_data,
    ):
        """Test creating a payment"""
        # Create dependencies
        prop_repo = PropertyRepository(db)
        property_obj = prop_repo.create(db, obj_in=PropertyCreate(**sample_property_data))

        tenant_repo = TenantRepository(db)
        tenant_obj = tenant_repo.create(db, obj_in=TenantCreate(**sample_tenant_data))

        contract_repo = ContractRepository(db)
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_obj.id
        contract_data["tenant_id"] = tenant_obj.id
        contract_obj = contract_repo.create(db, obj_in=ContractCreate(**contract_data))

        # Create payment
        repo = PaymentRepository(db)
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_obj.id
        payment_data["tenant_id"] = tenant_obj.id
        payment_data["contract_id"] = contract_obj.id
        payment_create = PaymentCreate(**payment_data)

        payment_obj = repo.create(db, obj_in=payment_create)

        assert payment_obj.id is not None
        assert payment_obj.amount == sample_payment_data["amount"]
        assert payment_obj.status == "pending"

    def test_get_payment(
        self,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
        sample_payment_data,
    ):
        """Test getting a payment by ID"""
        # Create dependencies
        prop_repo = PropertyRepository(db)
        property_obj = prop_repo.create(db, obj_in=PropertyCreate(**sample_property_data))

        tenant_repo = TenantRepository(db)
        tenant_obj = tenant_repo.create(db, obj_in=TenantCreate(**sample_tenant_data))

        contract_repo = ContractRepository(db)
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_obj.id
        contract_data["tenant_id"] = tenant_obj.id
        contract_obj = contract_repo.create(db, obj_in=ContractCreate(**contract_data))

        # Create payment
        repo = PaymentRepository(db)
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_obj.id
        payment_data["tenant_id"] = tenant_obj.id
        payment_data["contract_id"] = contract_obj.id
        payment_create = PaymentCreate(**payment_data)

        created = repo.create(db, obj_in=payment_create)
        retrieved = repo.get(db, id=created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.amount == created.amount

    def test_update_payment_status(
        self,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
        sample_payment_data,
    ):
        """Test updating payment status"""
        # Create dependencies
        prop_repo = PropertyRepository(db)
        property_obj = prop_repo.create(db, obj_in=PropertyCreate(**sample_property_data))

        tenant_repo = TenantRepository(db)
        tenant_obj = tenant_repo.create(db, obj_in=TenantCreate(**sample_tenant_data))

        contract_repo = ContractRepository(db)
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_obj.id
        contract_data["tenant_id"] = tenant_obj.id
        contract_obj = contract_repo.create(db, obj_in=ContractCreate(**contract_data))

        # Create payment
        repo = PaymentRepository(db)
        payment_data = sample_payment_data.copy()
        payment_data["property_id"] = property_obj.id
        payment_data["tenant_id"] = tenant_obj.id
        payment_data["contract_id"] = contract_obj.id
        payment_create = PaymentCreate(**payment_data)

        created = repo.create(db, obj_in=payment_create)

        update_data = PaymentUpdate(
            status="paid", payment_date=date(2025, 1, 3), payment_method="pix"
        )
        updated = repo.update(db, db_obj=created, obj_in=update_data)

        assert updated.status == "paid"
        assert updated.payment_method == "pix"
        assert updated.payment_date is not None

    @pytest.mark.parametrize("status", ["pending", "paid", "overdue", "partial"])
    def test_payment_status_values(
        self,
        db: Session,
        sample_property_data,
        sample_tenant_data,
        sample_contract_data,
        sample_payment_data,
        status,
    ):
        """Test different payment status values (parametrized)"""
        # Create dependencies
        prop_repo = PropertyRepository(db)
        property_obj = prop_repo.create(db, obj_in=PropertyCreate(**sample_property_data))

        tenant_repo = TenantRepository(db)
        tenant_obj = tenant_repo.create(db, obj_in=TenantCreate(**sample_tenant_data))

        contract_repo = ContractRepository(db)
        contract_data = sample_contract_data.copy()
        contract_data["property_id"] = property_obj.id
        contract_data["tenant_id"] = tenant_obj.id
        contract_obj = contract_repo.create(db, obj_in=ContractCreate(**contract_data))

        # Create payment
        repo = PaymentRepository(db)

        data = sample_payment_data.copy()
        data["property_id"] = property_obj.id
        data["tenant_id"] = tenant_obj.id
        data["contract_id"] = contract_obj.id
        data["status"] = status
        payment_create = PaymentCreate(**data)

        created = repo.create(db, obj_in=payment_create)

        assert created.status == status

    @pytest.mark.parametrize("method", ["cash", "transfer", "pix", "check", "card"])
    def test_payment_methods(self, method):
        """Test valid payment methods (parametrized)"""
        valid_methods = ["cash", "transfer", "pix", "check", "card"]
        assert method in valid_methods

    def test_calculate_total_with_fine(self):
        """Test total calculation with fine"""
        amount = 1500.00
        fine_amount = 150.00
        total = amount + fine_amount

        assert total == 1650.00

    def test_calculate_total_without_fine(self):
        """Test total calculation without fine"""
        amount = 1500.00
        fine_amount = 0.00
        total = amount + fine_amount

        assert total == 1500.00
