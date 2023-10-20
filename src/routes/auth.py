from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.repository import token as token_repository
from src.repository import users as users_repository
from src.schemas.users import (
    UserModel,
    UserResponse,
    TokenModel,
)
from src.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes in a UserModel object, which is validated by pydantic.
        If the email already exists, it will return an HTTP 409 error code (conflict).
        If the username already exists, it will return an HTTP 409 error code (conflict).
        If this a first user in database its created as 'admin'.
        Otherwise, it will create a new user and emailing to confirm their account.

        :param body: UserModel: Get the user's email and password from the request body
        :param db: Session: Get the database session
        :return: A dictionary with the user and a detail message
        :doc-author: yarmel
    """

    # email check
    if await users_repository.get_user_by_email(body.email, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    # username check
    if await users_repository.get_user_by_username(body.username, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This username already registered"
        )

    body.password = auth_service.get_password_hash(body.password)
    new_user = await users_repository.create_user(body, db)

    # first admin check
    if await users_repository.users_count(db) == 1:
        await users_repository.assign_admin_role(new_user, db)

    return {"user": new_user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    The login function is used to authenticate a user.

        :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
        :param db: Session: Get the database session
        :return: A dictionary with the access_token, refresh_token and token type
        :doc-author: yarmel
    """

    user = await users_repository.get_user_by_username(body.username, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    # Generate JWT
    access_token = await auth_service.create_access_token(
        data={"email": user.email}
    )
    refresh_token = await auth_service.create_refresh_token(
        data={"email": user.email}
    )

    await users_repository.update_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(access_token: str = Depends(auth_service.oauth2_scheme), db: Session = Depends(get_db)):
    """
    The logout function is used to logout a user.
        The function adding user access token to blacklist in database.

        :param access_token: str: Not decoded access token.
        :param db: Session: Access the database.
        :return: A dictionary with result of operation.
        :doc-author: yarmel
    """
    token_data = await auth_service.get_data_from_access_token(access_token, db)
    if await token_repository.add_token_to_blacklist(token_data.email, access_token, db):
        return {'result': "Logout successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns a new access_token and refresh_token pair.
        If the user's current refresh token does not match what was passed into this function, then it will return an error.

        :param credentials: HTTPAuthorizationCredentials: Retrieve the token from the header
        :param db: Session: Access the database
        :return: A dictionary with the access_token, refresh_token and token type
        :doc-author: yarmel
    """

    token = credentials.credentials
    token_data = await auth_service.get_data_from_refresh_token(token)
    user = await users_repository.get_user_by_email(token_data.email, db)

    if user.refresh_token != token:
        await users_repository.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    # Generate JWT
    access_token = await auth_service.create_access_token(
        data={"email": user.email}
    )
    refresh_token = await auth_service.create_refresh_token(
        data={"email": user.email}
    )

    await users_repository.update_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
