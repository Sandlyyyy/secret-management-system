# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine, Base
from app.api.endpoints import auth, secrets, requests, audit

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Secret Management System",
    description="Corporate secrets management with approval workflow",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(secrets.router, prefix="/api/v1/secrets", tags=["secrets"])
app.include_router(requests.router, prefix="/api/v1/requests", tags=["requests"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["audit"])

@app.get("/")
async def root():
    return {"message": "Secret Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}