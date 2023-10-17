from dataclasses import dataclass
from pathlib import Path
from ipaddress import ip_address

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, BeforeValidator, EmailStr
from fastapi.templating import Jinja2Templates
from config.conection_config import ALGORITHM, URL_DB, SECRET_KEY, CLOUDINARY_NAME, CLOUDINARY_API, \
    CLOUDINARY_API_SECRET, REDIS_DB_HOST, REDIS_DB_PORT, PASSWORD_REDIS

BASE_DIR = Path(__file__).parent


@dataclass(frozen=True)
class Template:
    emails: Path = BASE_DIR / 'src' / 'templates' / 'emails'
    html_response: Jinja2Templates = Jinja2Templates(directory=BASE_DIR / 'src' / 'templates' / 'response')


class Settings(BaseSettings):
    db_url: str = URL_DB

    secret_key_jwt: str = SECRET_KEY
    algorithm: str = ALGORITHM

    # mail_username: EmailStr
    # mail_password: str
    # mail_from: EmailStr
    # mail_port: int
    # mail_server: str
    # mail_from_name: str

    redis_host: str = REDIS_DB_HOST
    redis_port: int = REDIS_DB_PORT
    redis_password: str = PASSWORD_REDIS

    cloudinary_name: str = CLOUDINARY_NAME
    cloudinary_api_key: int = CLOUDINARY_API
    cloudinary_api_secret: str = CLOUDINARY_API_SECRET
    cloudinary_folder: str = "PyCrafters/"

    class Config:
        env_file = BASE_DIR / '.env'



settings = Settings()
