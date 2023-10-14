from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import User, Comment, Photo

from schemas import CommentModel

async def create_comment(photo_id: int, body: CommentModel, user: User, db: Session) -> Comment | None:
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        comment = Comment(body.model_dump())
        comment.user = user
        comment.photo = photo
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment


async def get_comments(photo_id: int, user: User, db: Session) -> List[Comment] | None:
    comments = db.query(Comment).filter(and_(Comment.user_id == user.id, Comment.photo_id == photo_id)).all()
    return comments


async def update_comment(comment_id: int, body: CommentModel, user: User, db: Session) -> Comment | None:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user.id)).first()
    if comment:
        comment.content = body.content
        db.commit()
    return comment


async def delete_comment(comment_id: int, user: User, db: Session) -> Comment | None:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user.id)).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
