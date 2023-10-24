from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.models import User
from src.repository import token as token_repository
from src.repository import users as users_repository
from src.schemas.users import (
    UserDb,
    UserResponse,
)
from src.services.auth import auth_service, TokenData
from src.services.users import users_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.patch("/clear")
async def clear_expires_tokens(
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The clear_expires_tokens function clear expires access tokens from database.
        Only for admins users.

        :param db: Session: Access the database.
        :param current_user: User: Get the current user from the auth_service.
        :return: A dictionary with result of operation.
        :doc-author: yarmel
    """
    if users_service.admin_check(current_user):
        await token_repository.clear_expires_records(db)
        return {"result": "Old blacklisted records was deleted"}


@router.patch("/assign", response_model=UserResponse)
async def assign_role(
        username: str,
        admin: bool = False,
        moderator: bool = False,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The function assign role for a user in the database. Only for admins users.
        The function takes in a token data and returns a user from database with new role.
        If user without 'admin' role try to do that it will return an error.
        If 'user_email' don't exist in database it will return an error.

        :param username: str: Specify a username for role assignation.
        :param admin: bool: Check for admin role.
        :param moderator: bool: Check for moderator role.
        :param current_user: User: Get the current user from the auth_service.
        :param db: Session: Access the database.
        :return: A dictionary with user with new role.
        :doc-author: yarmel
    """

    if users_service.admin_check(current_user):
        user = await users_service.get_user_by_username(username, db)
        if admin:
            user = await users_repository.assign_admin_role(user, db)
        else:
            user = await users_repository.remove_admin_role(user, db)
        if moderator:
            user = await users_repository.assign_moderator_role(user, db)
        else:
            user = await users_repository.remove_moderator_role(user, db)

        return {"user": user, "detail": "User role successfully assigned"}


@router.patch(
    "/ban",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=1))],
)
async def ban_user(
        username: str,
        banned: bool = True,
        current_user: TokenData = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The ban_user function set a user status in the database.
        Only for admins users.

        :param username: str: Specify a username for updating.
        :param banned: bool: Check for user status. Banned or active user.
        :param db: Session: Access the database.
        :param current_user: User: Get the current user from the auth_service.
        :return: A UserResponse model with updated user.
        :doc-author: yarmel
    """
    if users_service.admin_check(current_user):
        user = await users_service.get_user_by_username(username, db)
        if banned:
            user = await users_repository.add_ban_user(user, db)
            return {"user": user, "detail": "User are banned now"}
        else:
            user = await users_repository.remove_ban_user(user, db)
            return {"user": user, "detail": "User is active now"}


@router.get(
    "/getuser/{username}",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=1))],
)
async def get_user_data(
        username: str,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The get_user_data function takes a user data from database.
        Only for admins users.

        :param username: str: Specify a username for updating.
        :param db: Session: Access the database.
        :param current_user: User: Get the current user from the auth_service.
        :return: A UserResponse model with updated user.
        :doc-author: yarmel
    """
    if users_service.admin_check(current_user):
        user = await users_service.get_user_by_username(username, db)
        return {"user": user, "detail": "Actual user info"}


@router.patch(
    "/updateuser/{username}",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=1))],
)
async def update_user_data(
        username: str,
        body: UserDb,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    WARNING! Dangerous instrument! The update_user_data function updates a user in the database.
        Only for admins users.

        :param username: str: Specify a username for updating.
        :param body: UserDb: Specify the type of data that will be passed in the body.
        :param db: Session: Access the database.
        :param current_user: User: Get the current user from the auth_service.
        :return: A UserResponse model with updated user.
        :doc-author: yarmel
    """
    if users_service.admin_check(current_user):
        user = await users_service.get_user_by_username(username, db)
        updated_user = await users_repository.update_user(user, body, db)
        return {"user": updated_user, "detail": "User successfully updated"}


@router.delete(
    "/deleteuser/{username}",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=1))],
)
async def delete_user(
        username: str,
        current_user: TokenData = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The delete_user function delete a user from database.
        Only for admins users.

        :param username: str: Specify a username for deleting.
        :param db: Session: Access the database.
        :param current_user: User: Get the current user from the auth_service.
        :return: A UserResponse model with deleted user.
        :doc-author: yarmel
    """
    if users_service.admin_check(current_user):
        user = await users_service.get_user_by_username(username, db)
        deleted_user = await users_repository.delete_user(user, db)
        return {"user": deleted_user, "detail": "User successfully deleted"}
