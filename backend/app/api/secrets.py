from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.secret import Secret
from app.services.openbao_service import OpenBaoService
from cryptography.fernet import Fernet
import os
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/secrets", tags=["secrets"])
fernet_key = os.getenv("FERNET_KEY", Fernet.generate_key())
cipher = Fernet(fernet_key)

# Pydantic модели
class SecretResponse(BaseModel):
    id: int
    name: str
    description: str
    type: str

    class Config:
        from_attributes = True

class CreateSecret(BaseModel):
    name: str
    description: str
    type: str = "database"
    username: str
    password: str
    host: str = ""

@router.get("/", response_model=List[SecretResponse])
def get_secrets(db: Session = Depends(get_db)):
    secrets = db.query(Secret).all()
    return secrets

@router.post("/")
def create_secret(secret: CreateSecret, db: Session = Depends(get_db)):
    encrypted_password = cipher.encrypt(secret.password.encode()).decode()
    db_secret = Secret(
        name=secret.name,
        description=secret.description,
        type=secret.type,
        username=secret.username,
        password=encrypted_password,
        host=secret.host
    )
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    # Отправка в OpenBao
    OpenBaoService.save_secret(secret.name, secret.username, secret.password, secret.host)
    return {"message": "Secret saved", "secret_id": db_secret.id}

@router.get("/{name}")
def get_secret(name: str, db: Session = Depends(get_db)):
    secret = db.query(Secret).filter(Secret.name == name).first()
    if not secret:
        secret_data = OpenBaoService.get_secret(name)
        if not secret_data:
            raise HTTPException(status_code=404, detail="Secret not found")
        return secret_data
    decrypted_password = cipher.decrypt(secret.password.encode()).decode()
    return {
        "name": secret.name,
        "description": secret.description,
        "type": secret.type,
        "username": secret.username,
        "password": decrypted_password,
        "host": secret.host
    }