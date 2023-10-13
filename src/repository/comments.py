from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import User, Comment, Photo

from schemas import CommentModel

async def create_comment(body: CommentModel, photo: Photo, user: User, db: Session) -> Comment:
    comment = Comment(body.model_dump())
    comment.user = user
    comment.photo = photo
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def get_comments(photo: Photo, user: User, db: Session) -> List[Comment]:
    comments = db.query(Comment).filter(and_(User.id == user.id, Photo.id == photo.id)).all()
    return comments


async def update_comment(comment_id: int, body: CommentModel, user: User, db: Session) -> Comment | None:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, User.id == user.id)).first()
    if comment:
        comment.content = body.content
        db.commit()
    return comment


async def delete_comment(comment_id: int, user: User, db: Session) -> Comment | None:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, User.id == user.id)).first()
    db.delete(comment)
    db.commit()
    return comment
