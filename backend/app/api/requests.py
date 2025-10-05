from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.request import AccessRequest
from datetime import datetime
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/requests", tags=["requests"])

# Pydantic модели дл€ запросов
class CreateRequest(BaseModel):
    user_id: str = "current_user"
    user_name: str = "“екущий пользователь"
    secret_name: str
    description: str
    duration: int = 7
    type: str = "database"

class RequestResponse(BaseModel):
    id: int
    user_id: str
    user_name: str
    secret_name: str
    description: str
    status: str
    duration: int
    type: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[RequestResponse])
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(AccessRequest).order_by(AccessRequest.created_at.desc()).all()
    return requests

@router.post("/", response_model=RequestResponse)
def create_request(request: CreateRequest, db: Session = Depends(get_db)):
    db_request = AccessRequest(
        user_id=request.user_id,
        user_name=request.user_name,
        secret_name=request.secret_name,
        description=request.description,
        duration=request.duration,
        type=request.type
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/{request_id}/approve")
def approve_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = "approved"
    request.approved = True
    request.approved_at = datetime.utcnow()
    db.commit()
    return {"message": "Request approved"}

@router.post("/{request_id}/reject")
def reject_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = "rejected"
    request.approved = False
    request.rejected_at = datetime.utcnow()
    db.commit()
    return {"message": "Request rejected"}