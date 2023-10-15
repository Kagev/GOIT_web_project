from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from schemas import CommentModel, CommentResponse
from src.database.db import get_db
from src.database.models import User, Photo
from src.repository import comments as repository_comments
from src.service.auth import auth_service

router = APIRouter(prefix='/comments', tags=['comments'])


@router.post('/{photo_id}', response_model=CommentResponse)
async def create_comment(photo_id: int, body: CommentModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    comment = await repository_comments.create_comment(photo_id, body, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Photo not found')
    return comment


@router.get('/{photo_id}', response_model=List[CommentResponse])
async def get_comments(photo_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    comment = await repository_comments.get_comments(photo_id, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Photo not found')
    return comment


@router.patch('/{comment_id}', response_model=CommentResponse)
async def update_comment(comment_id: int, body: CommentModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    comment = await repository_comments.update_comment(comment_id, body, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    elif not ((current_user.role in ('admin', 'moderator')) or comment.user_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to perform this action')
    return comment


@router.delete('/{comment_id}', response_model=CommentResponse)
async def delete_comment(comment_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    comment = await repository_comments.delete_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    elif current_user.role not in ('admin', 'moderator'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to perform this action')
    return comment
