from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent
load_dotenv()


class Settings(BaseSettings):

	# Token block
	secret_key: str = os.environ.get('SECRET_KEY')
	algorithm: str = os.environ.get('ALGORITHM')
	expires_delta_access_token: int = os.environ.get('JWT_TOKEN')
	expires_delta_refresh_token: int = os.environ.get('REF_JWT_TOKEN')

	# Users block
	allowed_roles: list = ["user", "moderator", "admin"]

	# DB block
	postgres_name: str = os.environ.get("POSTGRES_DB_NAME")
	postgres_user: str = os.environ.get("USERNAME_ELEPHANT")
	postgres_password: str = os.environ.get("PASSWORD_ELEPHANT")
	postgres_domain: str = os.environ.get("POSTGRES_HOST")
	postgres_port: int = os.environ.get("POSTGRES_PORT")
	postgres_url: str = os.environ.get("URL_ELEPHANT")

	# Redis cloud
	REDIS_DB_NAME = os.environ.get("REDIS_DB_NAME")
	REDIS_ENDPOINT = os.environ.get("REDIS_DB_ENDPOINT")
	USERNAME_REDIS = os.environ.get("USERNAME_REDIS")
	PASSWORD_REDIS = os.environ.get("PASSWORD_REDIS")
	REDIS_DB_HOST = os.environ.get("REDIS_DB_HOST")
	REDIS_DB_PORT = os.environ.get("REDIS_DB_PORT")

	# Cloudinary
	CLOUDINARY_NAME = os.environ.get("CLOUD_NAME")
	CLOUDINARY_API = os.environ.get("CLOUD_API_KEY")
	CLOUDINARY_API_SECRET = os.environ.get("CLOUD_API_SECRET")
	CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")

	# LavinaMQ - analog RebbitMQ
	CLUSTER_MQ = os.environ.get("CLUSTER_MQ")
	HOST_MQ = os.environ.get("HOST_MQ")
	USERNAME_MQ = os.environ.get("USER_MQ")
	PASSWORD_MQ = os.environ.get("PASSWORD_MQ")
	URL_MQ = os.environ.get("URL_MQ")
	PORT_MQ = os.environ.get("PORT_MQ")
	TSL_PORT_MQ = os.environ.get("PORT_MQ_TSL")

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"
		case_sensitive = False


settings = Settings()
