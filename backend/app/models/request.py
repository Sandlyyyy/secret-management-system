from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from datetime import datetime
from app.database import Base

class AccessRequest(Base):
    __tablename__ = "access_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=False, default="Текущий пользователь")
    secret_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected
    duration = Column(Integer, default=7)
    type = Column(String, default="database")  # database, api, ssh
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)