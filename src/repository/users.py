from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas.users import UserModel


async def create_user(body: UserModel, db: Session) -> User:
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


async def users_count(db: Session) -> int:
    return int(db.execute(func.count(User.id)).scalar())


async def get_user_by_email(email: str, db: Session) -> Optional[User]:
    return db.execute(select(User).filter(User.email == email)).scalar()


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def assign_role(email: str, user_role: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.role = user_role
    db.commit()
    return user
