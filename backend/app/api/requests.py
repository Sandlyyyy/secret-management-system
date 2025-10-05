from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.request import AccessRequest
from datetime import datetime

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/")
def create_request(user_id: str, secret_name: str, db: Session = Depends(get_db)):
    request = AccessRequest(user_id=user_id, secret_name=secret_name)
    db.add(request)
    db.commit()
    db.refresh(request)
    return {"message": "Request created", "request_id": request.id}

@router.post("/{request_id}/approve")
def approve_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.approved = True
    request.approved_at = datetime.utcnow()
    db.commit()
    return {"message": "Request approved"}
