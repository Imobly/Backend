"""Unit tests for Properties module"""

import pytest
from sqlalchemy.orm import Session

from app.src.properties.repository import PropertyRepository
from app.src.properties.schemas import PropertyCreate, PropertyUpdate


class TestPropertyRepository:
    """Test Property Repository"""

    def test_create_property(self, db: Session, sample_property_data):
        """Test creating a property"""
        repo = PropertyRepository(db)
        property_create = PropertyCreate(**sample_property_data)

        property_obj = repo.create(db, obj_in=property_create)

        assert property_obj.id is not None
        assert property_obj.name == sample_property_data["name"]
        assert property_obj.address == sample_property_data["address"]
        assert property_obj.status == "vacant"

    def test_get_property(self, db: Session, sample_property_data):
        """Test getting a property by ID"""
        repo = PropertyRepository(db)
        property_create = PropertyCreate(**sample_property_data)

        created = repo.create(db, obj_in=property_create)
        retrieved = repo.get(db, id=created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == created.name

    def test_update_property(self, db: Session, sample_property_data):
        """Test updating a property"""
        repo = PropertyRepository(db)
        property_create = PropertyCreate(**sample_property_data)

        created = repo.create(db, obj_in=property_create)

        update_data = PropertyUpdate(status="occupied", rent=2000.00)
        updated = repo.update(db, db_obj=created, obj_in=update_data)

        assert updated.status == "occupied"
        assert updated.rent == 2000.00
        assert updated.name == sample_property_data["name"]

    def test_delete_property(self, db: Session, sample_property_data):
        """Test deleting a property"""
        repo = PropertyRepository(db)
        property_create = PropertyCreate(**sample_property_data)

        created = repo.create(db, obj_in=property_create)
        property_id = created.id

        repo.remove(db, id=property_id)

        deleted = repo.get(db, id=property_id)
        assert deleted is None

    def test_get_multi_properties(self, db: Session, sample_property_data):
        """Test getting multiple properties"""
        repo = PropertyRepository(db)

        # Create 3 properties
        for i in range(3):
            data = sample_property_data.copy()
            data["name"] = f"Property {i}"
            property_create = PropertyCreate(**data)
            repo.create(db, obj_in=property_create)

        # Get all
        properties = repo.get_multi(db, skip=0, limit=10)

        assert len(properties) == 3

    @pytest.mark.parametrize("status", ["vacant", "occupied", "maintenance", "inactive"])
    def test_property_status_validation(self, db: Session, sample_property_data, status):
        """Test property status values (parametrized)"""
        repo = PropertyRepository(db)

        data = sample_property_data.copy()
        data["status"] = status
        property_create = PropertyCreate(**data)

        created = repo.create(db, obj_in=property_create)

        assert created.status == status
