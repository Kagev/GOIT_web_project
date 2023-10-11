from dataclasses import dataclass
from pathlib import Path
from ipaddress import ip_address

from pydantic import BaseSettings, EmailStr
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent


@dataclass(frozen=True)
class Template:
    emails: Path = BASE_DIR / 'src' / 'templates' / 'emails'
    html_response: Jinja2Templates = Jinja2Templates(directory=BASE_DIR / 'src' / 'templates' / 'response')


class Settings(BaseSettings):
    db_url: str = "{DB_TYPE}+{DB_CONNECTOR}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    secret_key_jwt: str = "secret_key_jwt"
    algorithm: str = "HS256"

    mail_username: EmailStr
    mail_password: str
    mail_from: EmailStr
    mail_port: int
    mail_server: str
    mail_from_name: str

    redis_host: str
    redis_port: int
    redis_password: str

    cloudinary_name: str
    cloudinary_api_key: int
    cloudinary_api_secret: str
    cloudinary_folder: str = "folder/"

    class Config:
        env_file = BASE_DIR / '.env'


settings = Settings()
