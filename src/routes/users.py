from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas.users import UserProfileResponse, UserProfileUpdate
from src.services.auth import auth_service
from src.services.users import users_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/{username}",
    response_model=UserProfileResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=1))],
)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """
    The get_user_profile function get profile data of the specific user.
        All users have access.

        :param username: str: Specify the username for getting data.
        :param db: Session: Access the database.
        :return: A UserProfileResponse model with user data.
        :doc-author: yarmel
    """
    return await users_service.get_user_by_username(username, db)


@router.patch(
    "/my_info/{username}",
    response_model=UserProfileResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=1))],
)
async def edit_user_profile(
        username: str,
        body: UserProfileUpdate,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The edit_user_profile function provide editing access for a current user if he is profile owner.

        :param username: str: Specify the username for getting profile.
        :param body: UserProfileUpdate: Specify the type of data that will be passed in the body.
        :param current_user: User: Get the current user from the auth_service.
        :param db: Session: Access the database.
        :return: A UserProfileResponse model with user data.
        :doc-author: yarmel
    """

    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You don't have access to {username} profile",
        )

    return await repository_users.edit_user(username, body, db)
