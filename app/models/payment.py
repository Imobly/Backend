from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date)
    payment_method = Column(String(50))  # 'dinheiro', 'pix', 'transferencia', 'boleto'
    status = Column(String(20), default="pendente")  # 'pago', 'pendente', 'atrasado'
    reference_month = Column(String(7))  # Format: YYYY-MM
    late_fee = Column(Numeric(10, 2), default=0)
    discount = Column(Numeric(10, 2), default=0)
    observations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    contract = relationship("Contract", back_populates="payments")