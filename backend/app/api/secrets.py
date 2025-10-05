from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.secret import Secret
from app.services.openbao_service import OpenBaoService
from cryptography.fernet import Fernet
import os

router = APIRouter(prefix="/secrets", tags=["secrets"])
fernet_key = os.getenv("FERNET_KEY", Fernet.generate_key())
cipher = Fernet(fernet_key)

@router.post("/")
def create_secret(name: str, username: str, password: str, host: str = "", db: Session = Depends(get_db)):
    encrypted_password = cipher.encrypt(password.encode()).decode()
    secret = Secret(name=name, username=username, password=encrypted_password, host=host)
    db.add(secret)
    db.commit()
    db.refresh(secret)
    # Отправка в OpenBao
    OpenBaoService.save_secret(name, username, password, host)
    return {"message": "Secret saved", "secret_id": secret.id}

@router.get("/{name}")
def get_secret(name: str, db: Session = Depends(get_db)):
    secret = db.query(Secret).filter(Secret.name == name).first()
    if not secret:
        secret_data = OpenBaoService.get_secret(name)
        if not secret_data:
            raise HTTPException(status_code=404, detail="Secret not found")
        return secret_data
    decrypted_password = cipher.decrypt(secret.password.encode()).decode()
    return {"name": secret.name, "username": secret.username, "password": decrypted_password, "host": secret.host}
