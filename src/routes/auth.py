from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr

from src.database.connection import get_db
from src.repository import users as repository_users
from src.repository.token_blacklist import add_token_to_blacklist, is_token_blacklisted, clear_expires_records
from src.services.auth import auth_service
from src.shemas.users import (
    UserModel,
    UserResponse,
    TokenModel,
    UserDb,
    role_in_allowed_roles,
)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    """The signup function creates a new user in the database."""

    # email check
    if await repository_users.get_user_by_email(body.email, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    # first admin check
    if await repository_users.users_count(db) == 1:
        await repository_users.assign_role(new_user.email, "admin", db)

    return {"user": new_user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """The login function is used to authenticate a user."""

    user = await repository_users.get_user_by_email(body.username, db)

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
        data={"email": user.email, "role": user.role}
    )
    refresh_token = await auth_service.create_refresh_token(
        data={"email": user.email, "role": user.role}
    )

    await repository_users.update_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(token: str = Depends(auth_service.get_current_user_token), db: Session = Depends(get_db)):
    """The logout function is used to authenticate a user."""
    email = await auth_service.get_email_from_token(token)
    if add_token_to_blacklist(email, token, db):
        return {'result': "Logout successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


@router.patch("/clear_expires_tokens")
async def clear_expires_tokens(
        db: Session = Depends(get_db)
):
    """The function delete old blacklisted records in the database."""

    clear_expires_records(db)
    return {"result": "Old blacklisted records was deleted"}


@router.patch("/assign_role", response_model=UserDb)
async def assign_role(
    user_email: EmailStr,
    new_role: str = "moderator",
    db: Session = Depends(get_db),
    token: str = Depends(auth_service.get_current_user_token),
):
    """The function assign role for a user in the database.
    Allowed roles: 'user', 'moderator', 'admin'. Only for admin users."""
    if not is_token_blacklisted(token, db):
        role = await auth_service.get_user_role_from_token(token)
        if role == "admin":
            exist_user = await repository_users.get_user_by_email(user_email, db)
            if not exist_user:
                raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail=f"Account with email {user_email} not exists",
                )
            if exist_user.role == new_role:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User already with '{new_role}' role!",
                )
            try:
                return await repository_users.assign_role(
                    user_email, role_in_allowed_roles(new_role), db
                )
            except AssertionError:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"Role '{new_role}' is not valid",
                )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admins can do this"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="This token is no valid. Try to login."
    )


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """The refresh_token function is used to refresh the access token."""
    token = credentials.credentials
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)

    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    # Generate JWT
    access_token = await auth_service.create_access_token(
        data={"email": user.email, "role": user.role}
    )
    refresh_token = await auth_service.create_refresh_token(
        data={"email": user.email, "role": user.role}
    )

    await repository_users.update_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
