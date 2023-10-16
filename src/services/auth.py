from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel


from config.conection_config import SECRET_KEY, ALGORITHM


class TokenData(BaseModel):
    username: str = None
    email: str = None
    role: str = None


class Auth:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(self) -> bool:
        pass

    def get_password_hash(self) -> str:
        pass

    def __decode_jwt(self) -> dict:
        pass

    def __encode_jwt(self) -> str:
        pass

    # define a function to generate a new access token
    async def create_access_token(self) -> str:
        pass

    # define a function to generate a new refresh token
    async def create_refresh_token(self) -> str:
        pass

    # define a function to generate a new confirmed email token
    async def create_email_token(self) -> str:
        pass

    async def decode_refresh_token(self) -> str:
        pass

    def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            role = payload.get("role")
            if username is None or role is None:
                raise credentials_exception
            token_data = TokenData(username=username, role=role)
        except JWTError:
            raise credentials_exception
        return token_data

    def get_current_user_as_admin(current_user: TokenData = Depends(get_current_user)):
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return current_user

    def get_current_user_as_moderator(
        current_user: TokenData = Depends(get_current_user),
    ):
        if current_user.role != "moderator":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return current_user

    async def get_email_from_token(self) -> str:
        pass


auth_service = Auth()
