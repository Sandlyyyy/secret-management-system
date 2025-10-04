from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://backend_user:backend_db_pass_123@postgres:5432/secret_management")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class SecretRequest(Base):
    __tablename__ = "secret_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    secret_name = Column(String, index=True)
    secret_type = Column(String)
    justification = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secret Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Secret Management System API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/secret-requests")
async def get_secret_requests(db: SessionLocal = Depends(get_db)):
    return db.query(SecretRequest).all()

@app.post("/api/secret-requests")
async def create_secret_request(request: dict, db: SessionLocal = Depends(get_db)):
    db_request = SecretRequest(
        user_id=request.get("user_id", "demo-user"),
        secret_name=request.get("secret_name"),
        secret_type=request.get("secret_type", "database"),
        justification=request.get("justification", "Demo request")
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)