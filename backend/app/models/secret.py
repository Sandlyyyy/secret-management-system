from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    host = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
