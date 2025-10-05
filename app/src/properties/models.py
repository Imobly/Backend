from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Numeric, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    type = Column(String(50), nullable=False)  # 'apartment', 'house', 'commercial', 'studio'
    area = Column(Numeric(10, 2), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    parking_spaces = Column(Integer, default=0)
    rent = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="vacant")  # 'vacant', 'occupied', 'maintenance', 'inactive'
    description = Column(Text)
    images = Column(JSON)  # Array de URLs das imagens
    is_residential = Column(Boolean, default=True)
    tenant = Column(String(255), nullable=True)  # Nome do inquilino atual
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    units = relationship("Unit", back_populates="property", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="property")
    payments = relationship("Payment", back_populates="property")
    expenses = relationship("Expense", back_populates="property")
    # maintenances = relationship("Maintenance", back_populates="property")  