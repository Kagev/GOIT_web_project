from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import User, Comment, Photo

from schemas import CommentModel

async def create_comment(photo_id: int, body: CommentModel, user: User, db: Session) -> Comment | None:
    """
    Creates new comment for specific Photo by specific User.

    :param photo_id: ID of Photo for which comment will be added.
    :type photo_id: int
    :param body: Data to create comment.
    :type body: CommentModel
    :param user: User by whose comment will be created.
    :type user: User
    :param db: Database session.
    :type db: Session
    :return: Created comment or None if Photo does not exist.
    :rtype: Comment | None
    """

    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        comment = Comment(body.model_dump())
        comment.user = user
        comment.photo = photo
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment


async def get_comments(photo_id: int, db: Session) -> List[Comment] | None:
    """
    Gets list of comments of specific Photo.

    :param photo_id: ID of Photo from which comments will be gotten.
    :type photo_id: int
    :param db: Database session.
    :type db: Session
    :return: List of comments or None if Photo does not exist.
    :rtype: List[Comment] | None
    """

    comments = db.query(Comment).filter(Comment.photo_id == photo_id).all()
    return comments


async def update_comment(comment_id: int, body: CommentModel, user: User, db: Session) -> Comment | None:
    """
    Updates specific comment by specific User.

    :param comment_id: ID of comment which will be updated.
    :type comment_id: int
    :param body: Data to update comment.
    :type body: CommentModel
    :param user: User by whose comment will be updated.
    :type user: User
    :param db: Database session.
    :type db: Session
    :return: Updated comment or None if comment does not exist.
    :rtype: Comment | None
    """

    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user.id)).first()
    if comment:
        comment.content = body.content
        db.commit()
    return comment


async def delete_comment(comment_id: int, user: User, db: Session) -> Comment | None:
    """
    Deletes specific comment by a specific user (ONLY BY MODER OR ADMIN).

    :param comment_id: ID of comment which will be deleted.
    :type comment_id: int
    :param user: User by whose comment will be deleted (ONLY MODER OR ADMIN).
    :type user: User
    :param db: Database session.
    :type db: Session
    :return: Deleted comment or None if comment does not exist.
    :rtype: Comment | None
    """

    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user.id)).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
