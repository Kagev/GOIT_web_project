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
	"""

	"""
	# env_file = ".env"
	env_file = env_path
	env_file_encoding = "utf-8"
	case_sensitive = False


class Settings(BaseSettings):
	# Token block
	expires_delta_access_token: str = os.getenv('JWT_TOKEN')
	expires_delta_refresh_token: str = os.getenv('REF_JWT_TOKEN')
	algorithm: str = os.getenv('ALGORITHM')
	secret_key: str = os.getenv('SECRET_KEY')

	# DB block
	postgres_name: str = os.getenv("POSTGRES_DB_NAME")
	postgres_user: str = os.getenv("POSTGRES_USERNAME")
	postgres_password: str = os.getenv("POSTGRES_PASSWORD")
	postgres_domain: str = os.getenv("POSTGRES_HOST")
	postgres_port: str = os.getenv("POSTGRES_PORT")
	postgres_url: str = os.getenv("POSTGRES_URL")

	# Users block
	allowed_roles: list = ["user", "moderator", "admin"]

	# Redis cloud
	redis_db_name: str = os.getenv("REDIS_DB_NAME")
	redis_endpoint: str = os.getenv("REDIS_DB_ENDPOINT")
	redis_username: str = os.getenv("REDIS_USERNAME")
	redis_password: str = os.getenv("REDIS_PASSWORD")
	redis_host: str = os.getenv("REDIS_DB_HOST")
	redis_port: int = os.getenv("REDIS_DB_PORT")
	redis_url: str = os.getenv("REDIS_URL")
	# Cloudinary
	cloudinary_name: str = os.getenv("CLOUDINARY_NAME")
	cloudinary_api: str = os.getenv("CLOUDINARY_API_KEY")
	cloudinary_api_secret: str = os.getenv("CLOUDINARY_API_SECRET")
	cloudinary_url: str = os.getenv("CLOUDINARY_URL")

	# LavinaMQ - analog RebbitMQ
	lavina_cluster: str = os.getenv("LAVINA_CLUSTER")
	lavina_host: str = os.getenv("LAVINA_HOST")
	lavina_user: str = os.getenv("LAVINA_USER")
	lavina_password: str = os.getenv("LAVINA_PASSWORD")
	lavina_url: str = os.getenv("LAVINA_URL")
	lavina_port: int = os.getenv("LAVINA_PORT")
	lavina_port_tsl: int = os.getenv("LAVINA_PORT_TSL")


settings = Settings()
