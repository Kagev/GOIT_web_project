from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ImageData
from qr_schemas import CommentModel, CommentResponse

router = APIRouter()

@router.post("/comments/", response_model=CommentResponse)
def create_comment(comment: CommentModel, db: Session = Depends(get_db)):
    db_comment = ImageData(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
