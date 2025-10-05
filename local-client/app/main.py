from fastapi import FastAPI
from app.api import secrets, requests
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secret Management System")

app.include_router(secrets.router)
app.include_router(requests.router)

@app.get("/health")
def health():
    return {"status": "ok"}
