from fastapi import FastAPI
from app.api import secrets
from app.db import models, database

app = FastAPI(title="Secret Manager Backend")

models.Base.metadata.create_all(bind=database.engine)
app.include_router(secrets.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
