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
	# env_file = ".env"
	env_file = env_path
	env_file_encoding = "utf-8"
	case_sensitive = False


class Settings(BaseSettings):
	# DB block
	postgres_name: str = os.getenv("POSTGRES_DB_NAME")
	postgres_user: str = os.getenv("USERNAME_ELEPHANT")
	postgres_password: str = os.getenv("PASSWORD_ELEPHANT")
	postgres_domain: str = os.getenv("POSTGRES_HOST")
	postgres_port: str = os.getenv("POSTGRES_PORT")
	postgres_url: str = os.getenv("URL_ELEPHANT")

	# Token block
	algorithm: str = os.getenv('ALGORITHM')
	expires_delta_access_token: str = os.getenv('JWT_TOKEN')
	expires_delta_refresh_token: str = os.getenv('REF_JWT_TOKEN')
	secret_key: str = os.getenv('SECRET_KEY')

	# Users block
	allowed_roles: list = ["user", "moderator", "admin"]

	# Redis cloud
	redis_db_name: str = os.getenv("REDIS_DB_NAME")
	redis_endpoint: str = os.getenv("REDIS_DB_ENDPOINT")
	redis_username: str = os.getenv("USERNAME_REDIS")
	redis_password: str = os.getenv("PASSWORD_REDIS")
	redis_db_host: str = os.getenv("REDIS_DB_HOST")
	redis_db_port: int = os.getenv("REDIS_DB_PORT")

	# Cloudinary
	cloudinary_name: str = os.getenv("CLOUDINARY_NAME")
	cloudinary_api: str = os.getenv("CLOUDINARY_API_KEY")
	cloudinary_api_secret: str = os.getenv("CLOUDINARY_API_SECRET")
	cloudinary_url: str = os.getenv("CLOUDINARY_URL")

	# LavinaMQ - analog RebbitMQ
	lavina_cluster: str = os.getenv("CLUSTER_MQ")
	lavina_host: str = os.getenv("HOST_MQ")
	lavina_user: str = os.getenv("USER_MQ")
	lavina_password: str = os.getenv("PASSWORD_MQ")
	lavina_url: str = os.getenv("URL_MQ")
	lavina_port: int = os.getenv("PORT_MQ")
	lavina_port_tsl: int = os.getenv("PORT_MQ_TSL")


settings = Settings()
