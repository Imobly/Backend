from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Maintenance(Base):
    __tablename__ = "maintenances"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # 'hidraulica', 'eletrica', 'pintura', 'geral'
    priority = Column(String(20), default="media")  # 'baixa', 'media', 'alta', 'urgente'
    status = Column(String(20), default="aberto")  # 'aberto', 'em_andamento', 'concluido', 'cancelado'
    cost = Column(Numeric(10, 2))
    contractor_name = Column(String(255))
    contractor_contact = Column(String(255))
    scheduled_date = Column(Date)
    completion_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    property = relationship("Property", back_populates="maintenances")