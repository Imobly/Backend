from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(Text, nullable=False)
    property_type = Column(String(50), nullable=False)  # 'apartamento', 'casa', 'comercial'
    area = Column(Numeric(10, 2))
    rooms = Column(Integer)
    bathrooms = Column(Integer)
    description = Column(Text)
    monthly_rent = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="disponivel")  # 'ocupado', 'disponivel', 'manutencao'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    contracts = relationship("Contract", back_populates="property")
    maintenances = relationship("Maintenance", back_populates="property")