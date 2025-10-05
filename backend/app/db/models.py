from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from datetime import datetime

class SecretRequest(Base):
    __tablename__ = "secret_requests"
    id = Column(Integer, primary_key=True, index=True)
    secret_name = Column(String, nullable=False)
    requester = Column(String, nullable=False)
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Secret(Base):
    __tablename__ = "secrets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    encrypted_value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
