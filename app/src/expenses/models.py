from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String(20), nullable=False)  # 'expense', 'maintenance'
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    status = Column(String(20), nullable=False)  # 'pending', 'paid', 'scheduled'
    priority = Column(String(20), nullable=True)  # 'low', 'medium', 'high', 'urgent'
    vendor = Column(String(255), nullable=True)
    receipt = Column(Text, nullable=True)  # URL do comprovante
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    property = relationship("Property", back_populates="expenses")