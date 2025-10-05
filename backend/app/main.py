from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import secrets, requests
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secret Management System")

# Настройка CORS для SPA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Адрес вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(secrets.router)
app.include_router(requests.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Secret Management System API"}