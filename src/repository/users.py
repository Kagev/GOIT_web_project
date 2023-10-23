from typing import Optional

from sqlalchemy import select, func, update
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.users import UserModel, UserDb, UserProfileUpdate


async def create_user(body: UserModel, db: Session) -> User:
    """
    The function adding user in database.
        It takes user data and add it in database, return dictionary if successful.

    :param body: UserModel: User model object, which is validated by pydantic.
    :param db: Session: Get the database session
    :return: A dictionary with the user.
    :doc-author: yarmel
    """
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


async def users_count(db: Session) -> int:
    """
    The function count users in database.
        Just return count of user in database.

    :param db: Session: Get the database session
    :return: int value with count of users.
    :doc-author: yarmel
    """
    return int(db.execute(func.count(User.id)).scalar())


async def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """
    The function count users in database.
        It will try to find user in database by using email.

    :param email: str: User email.
    :param db: Session: Get the database session
    :return: User data.
    :doc-author: yarmel
    """
    return db.execute(select(User).filter(User.email == email)).scalar()


async def get_user_by_username(username: str, db: Session) -> Optional[User]:
    """
    The function count users in database.
        It will try to find user in database by using email.

    :param username: str: User username.
    :param db: Session: Get the database session
    :return: User data.
    :doc-author: yarmel
    """
    return db.execute(select(User).filter(User.username == username)).scalar()


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The function update user token in database.
        It will update user token in database.

    :param user: User: User email.
    :param token: str | None: Token.
    :param db: Session: Get the database session
    :return: None.
    :doc-author: yarmel
    """
    user.refresh_token = token
    db.commit()


async def assign_admin_role(user: User, db: Session) -> User:
    """
    The assign_admin_role assigning admin role to a user in the database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object after assigned.
    :doc-author: yarmel
    """
    user.is_admin = True
    db.commit()
    return user


async def remove_admin_role(user: User, db: Session) -> User:
    """
    The remove_admin_role function removes admin role from a user in the database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object after removing.
    :doc-author: yarmel
    """
    user.is_admin = False
    db.commit()
    return user


async def assign_moderator_role(user: User, db: Session) -> User:
    """
    The assign_moderator_role assigning moderator role to a user in the database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object after assigned.
    :doc-author: yarmel
    """
    user.is_moderator = True
    db.commit()
    return user


async def remove_moderator_role(user: User, db: Session) -> User:
    """
    The remove_moderator_role function removes moderator role from a user in the database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object after removing.
    :doc-author: yarmel
    """
    user.is_moderator = False
    db.commit()
    return user


async def edit_user(username: str, body: UserProfileUpdate, db: Session) -> Optional[User]:
    """
    The edit_user function updates a user in the database.

    :param username: str: Username string from user input.
    :param body: UserDb: Pass the data to be updated.
    :param db: Session: Access the database.
    :return: User object after updating.
    :doc-author: yarmel
    """
    user_body = {key: val for key, val in body.dict().items() if val is not None}

    user = db.execute(
        update(User)
        .values(**user_body)
        .filter((User.username == username))
        .returning(User)
    ).scalar()

    db.commit()

    return user


async def update_user(user: User, body: UserDb, db: Session) -> Optional[User]:
    """
    The update_user function updates a user in the database.

    :param user: User: User object from database.
    :param body: UserDb: Pass the data to be updated.
    :param db: Session: Access the database.
    :return: User object after updating.
    :doc-author: yarmel
    """
    user_body = {key: val for key, val in body.dict().items() if val is not None}

    user = db.execute(
        update(User)
        .values(**user_body)
        .filter((User.email == user.email))
        .returning(User)
    ).scalar()

    db.commit()

    return user


async def add_ban_user(user: User, db: Session) -> User:
    """
    The add_ban_user function add a ban status to a user in database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object after adding.
    :doc-author: yarmel
    """
    user.is_banned = True
    db.commit()
    return user


async def remove_ban_user(user: User, db: Session) -> User:
    """
    The remove_ban_user function removes a ban status from user in database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object after removing.
    :doc-author: yarmel
    """
    user.is_banned = False
    db.commit()
    return user


async def delete_user(user: User, db: Session) -> Optional[User]:
    """
    The delete_user function delete a user from the database.

    :param user: User: User object from database.
    :param db: Session: Access the database.
    :return: User object before deleted.
    :doc-author: yarmel
    """
    db.delete(user)
    db.commit()
    return user
