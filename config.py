from pydantic_settings import BaseSettings
from pathlib import Path
# from config.conection_config import ALGORITHM, URL_DB, SECRET_KEY, CLOUDINARY_NAME, CLOUDINARY_API, \
# 	CLOUDINARY_API_SECRET, REDIS_DB_HOST, REDIS_DB_PORT, PASSWORD_REDIS, JWT_TOKEN, REF_JWT_TOKEN, POSTGRES_PORT

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
	# DB block

	postgres_user: str = USERNAME_ELEPHANT
	postgres_password: str = PASSWORD_ELEPHANT
	postgres_name: str = POSTGRES_DB_NAME
	postgres_domain: str = POSTGRES_HOST
	postgres_port: int = POSTGRES_PORT

	# # REDIS block
	redis_host: str = REDIS_DB_HOST
	redis_port: int = REDIS_DB_PORT
	#
	# # Mail block
	# mail_username: str
	# mail_password: str
	# mail_from: str
	# mail_port: int
	# mail_server: str
	#
	# # Cloudinary block
	# cloudinary_name: str
	# cloudinary_api_key: int
	# cloudinary_api_secret: str
	# cloudinary_folder: str = "PyCrafters/"

	# Token block
	secret_key: str = SECRET_KEY
	algorithm: str = ALGORITHM
	expires_delta_access_token: int = JWT_TOKEN
	expires_delta_refresh_token: int = REF_JWT_TOKEN

	# Users block
	allowed_roles: list = ["user", "moderator", "admin"]

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"
		case_sensitive = False


settings = Settings()
