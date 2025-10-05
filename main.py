from fastapi import FastAPI
from db import database, models
from api import secrets

app = FastAPI(title="Secret Management System")

# Создаем таблицы при старте (для MVP)
models.Base.metadata.create_all(bind=database.engine)

# Подключаем роутеры
app.include_router(secrets.router)

@app.get("/")
def root():
    return {"message": "Secret Manager Backend is running"}
