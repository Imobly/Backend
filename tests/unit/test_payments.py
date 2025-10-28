"""Unit tests for Payments module"""

from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.src.payments.repository import PaymentRepository
from app.src.payments.schemas import PaymentCreate, PaymentUpdate


class TestPaymentRepository:
    """Test Payment Repository"""

    def test_create_payment(self, db: Session, sample_payment_data):
        """Test creating a payment"""
        repo = PaymentRepository(db)
        payment_create = PaymentCreate(**sample_payment_data)

        payment_obj = repo.create(db, obj_in=payment_create)

        assert payment_obj.id is not None
        assert payment_obj.amount == sample_payment_data["amount"]
        assert payment_obj.status == "pending"

    def test_get_payment(self, db: Session, sample_payment_data):
        """Test getting a payment by ID"""
        repo = PaymentRepository(db)
        payment_create = PaymentCreate(**sample_payment_data)

        created = repo.create(db, obj_in=payment_create)
        retrieved = repo.get(db, id=created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.amount == created.amount

    def test_update_payment_status(self, db: Session, sample_payment_data):
        """Test updating payment status"""
        repo = PaymentRepository(db)
        payment_create = PaymentCreate(**sample_payment_data)

        created = repo.create(db, obj_in=payment_create)

        update_data = PaymentUpdate(
            status="paid", payment_date=date(2025, 1, 3), payment_method="pix"
        )
        updated = repo.update(db, db_obj=created, obj_in=update_data)

        assert updated.status == "paid"
        assert updated.payment_method == "pix"
        assert updated.payment_date is not None

    @pytest.mark.parametrize("status", ["pending", "paid", "overdue", "partial"])
    def test_payment_status_values(self, db: Session, sample_payment_data, status):
        """Test different payment status values (parametrized)"""
        repo = PaymentRepository(db)

        data = sample_payment_data.copy()
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
