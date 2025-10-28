from datetime import datetime

from sqlalchemy import JSON, Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    profession = Column(String(100), nullable=False)
    emergency_contact = Column(JSON)  # {name, phone, relationship}
    documents = Column(JSON)  # Array de documentos {id, name, type, url}
    status = Column(String(20), default="active")  # 'active', 'inactive'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    contracts = relationship("Contract", back_populates="tenant")
    payments = relationship("Payment", back_populates="tenant")
