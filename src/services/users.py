from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.models import User
from src.repository import users as users_repository


class Users:

    async def get_user_by_email(self, user_email: str, db: Session = get_db) -> User:
        user = await users_repository.get_user_by_email(user_email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user_email} not found"
            )
        return user

    async def get_user_by_username(self, username: str, db: Session = get_db) -> User:
        user = await users_repository.get_user_by_username(username, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found"
            )
        return user

    async def user_check(self, user: User) -> bool:
        if user.is_banned:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are banned. Pray for mercy."
            )
        return True

    async def admin_check(self, user: User) -> bool:
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only Admins can do this",
            )
        return True


users_service = Users()
