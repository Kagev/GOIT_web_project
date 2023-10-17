from datetime import datetime, timedelta

from typing import Optional

from sqlalchemy.orm import Session

from pydantic import BaseModel
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings

from src.database.models import User
from src.database.connection import get_db
from src.repository.users import get_user_by_email
from src.repository.token_blacklist import is_token_blacklisted


class TokenData(BaseModel):
    email: Optional[str]
    role: Optional[str]


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    expires_delta_access_token = settings.expires_delta_access_token
    expires_delta_refresh_token = settings.expires_delta_refresh_token

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def __decode_jwt(self, token: str) -> dict:
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

    def __encode_jwt(self, data: dict, iat: datetime, exp: datetime, scope: str) -> str:
        to_encode = data.copy()
        to_encode.update({"iat": iat, "exp": exp, "scope": scope})

        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ) -> str:
        expire = datetime.utcnow() + (
            timedelta(minutes=expires_delta)
            if expires_delta
            else timedelta(self.expires_delta_access_token)
        )
        return self.__encode_jwt(data, datetime.utcnow(), expire, "access_token")

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ) -> str:
        expire = datetime.utcnow() + (
            timedelta(minutes=expires_delta)
            if expires_delta
            else timedelta(self.expires_delta_refresh_token)
        )
        return self.__encode_jwt(data, datetime.utcnow(), expire, "refresh_token")

    async def get_token_data(
        self, access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ) -> TokenData:
        if not await is_token_blacklisted(access_token, db):
            try:
                payload = self.__decode_jwt(access_token)

                if payload.get("scope") == "access_token":
                    user_email = payload.get("email")
                    user_role = payload.get("role")
                    return TokenData(email=user_email, role=user_role)

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid scope for token",
                )
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This token is no more valid. Login.",
        )

    async def get_data_from_refresh_token(self, refresh_token: str) -> TokenData:
        try:
            payload = self.__decode_jwt(refresh_token)

            if payload.get("scope") == "refresh_token":
                user_email = payload.get("email")
                user_role = payload.get("role")
                return TokenData(email=user_email, role=user_role)

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ) -> User:
        token_data = await self.get_token_data(access_token, db)
        current_user = await get_user_by_email(token_data.email, db)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"Account with email {token_data.email} not exists",
            )
        return current_user


auth_service = Auth()