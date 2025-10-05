from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/secrets", tags=["secrets"])

class SecretRequestCreate(BaseModel):
    secret_name: str
    requester: str

class SecretCreate(BaseModel):
    name: str
    encrypted_value: str

@router.post("/request")
def create_request(request: SecretRequestCreate, db: Session = Depends(database.get_db)):
    db_request = models.SecretRequest(secret_name=request.secret_name, requester=request.requester)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/approve")
def approve_request(request_id: int, db: Session = Depends(database.get_db)):
    db_request = db.query(models.SecretRequest).filter(models.SecretRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    db_request.approved = True
    db.commit()
    return {"message": "Request approved"}

@router.get("/{secret_id}")
def get_secret(secret_id: int, db: Session = Depends(database.get_db)):
    db_secret = db.query(models.Secret).filter(models.Secret.id == secret_id).first()
    if not db_secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    return db_secret
