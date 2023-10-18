"""
Configuration file. Take connect parametrs from .env
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# load_dotenv()

class Config:
	env_file = env_path
	env_file_encoding = "utf-8"
	case_sensitive = False


class Settings(BaseSettings):
	# Token block
	secret_key: str = os.getenv('SECRET_KEY')
	algorithm: str = os.getenv('ALGORITHM')
	expires_delta_access_token: str = os.getenv('JWT_TOKEN')
	expires_delta_refresh_token: str = os.getenv('REF_JWT_TOKEN')

	# Users block
	allowed_roles: list = ["user", "moderator", "admin"]

	# DB block
	postgres_name: str = os.getenv("POSTGRES_DB_NAME")
	postgres_user: str = os.getenv("USERNAME_ELEPHANT")
	postgres_password: str = os.getenv("PASSWORD_ELEPHANT")
	postgres_domain: str = os.getenv("POSTGRES_HOST")
	postgres_port: str = os.getenv("POSTGRES_PORT")
	postgres_url: str = os.getenv("URL_ELEPHANT")

	# Redis cloud
	REDIS_DB_NAME: str = os.getenv("REDIS_DB_NAME")
	REDIS_ENDPOINT: str = os.getenv("REDIS_DB_ENDPOINT")
	USERNAME_REDIS: str = os.getenv("USERNAME_REDIS")
	PASSWORD_REDIS: str = os.getenv("PASSWORD_REDIS")
	REDIS_DB_HOST: str = os.getenv("REDIS_DB_HOST")
	REDIS_DB_PORT: int = os.getenv("REDIS_DB_PORT")

	# Cloudinary
	CLOUDINARY_NAME: str = os.getenv("CLOUD_NAME")
	CLOUDINARY_API: str = os.getenv("CLOUD_API_KEY")
	CLOUDINARY_API_SECRET: str = os.getenv("CLOUD_API_SECRET")
	CLOUDINARY_URL: str = os.getenv("CLOUDINARY_URL")

	# LavinaMQ - analog RebbitMQ
	CLUSTER_MQ: str = os.getenv("CLUSTER_MQ")
	HOST_MQ: str = os.getenv("HOST_MQ")
	USERNAME_MQ: str = os.getenv("USER_MQ")
	PASSWORD_MQ: str = os.getenv("PASSWORD_MQ")
	URL_MQ: str = os.getenv("URL_MQ")
	PORT_MQ: int = os.getenv("PORT_MQ")
	TSL_PORT_MQ: int = os.getenv("PORT_MQ_TSL")


settings = Settings()
