from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String, default="database")  # database, api, ssh
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    host = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)