"""
configuration file for connecting the program with cloud services such as Redis, Cloudinary, ElephanSQL, and others
"""

from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# SECRET
JWT_TOKEN = os.environ.get('JWT_TOKEN')
REF_JWT_TOKEN = os.environ.get('REF_JWT_TOKEN')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

# cloud db (ElephanSQL)
POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME")
USERNAME_DB = os.environ.get("USERNAME_ELEPHANT")
PASSWORD_DB = os.environ.get("PASSWORD_ELEPHANT")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
URL_DB = os.environ.get("URL_ELEPHANT")
API_DB = os.environ.get("API_ELEPHANT")
DB_TYPE = os.environ.get("DB_TYPE")

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
