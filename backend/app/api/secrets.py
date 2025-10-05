from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/secrets", tags=["secrets"])

class SecretRequestCreate(BaseModel):
    secret_name: str
    requester: str

@router.post("/request")
def create_request(req: SecretRequestCreate, db: Session = Depends(database.get_db)):
    db_req = models.SecretRequest(secret_name=req.secret_name, requester=req.requester)
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

@router.get("/{request_id}")
def get_request(request_id: int, db: Session = Depends(database.get_db)):
    req = db.query(models.SecretRequest).filter(models.SecretRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req
