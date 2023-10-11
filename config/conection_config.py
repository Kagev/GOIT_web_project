"""
configuration file for connecting the program with cloud services such as Redis, Cloudinary, ElephanSQL, and others
"""

from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# cloud db (ElephanSQL)
POSTGRES_DB_NAME = os.environ.get("postgres_db_name")
USERNAME_DB = os.environ.get("username_elephant")
PASSWORD_DB = os.environ.get("password_elephant")
URL_DB = os.environ.get("url_elephant")
API_DB = os.environ.get("api_elephant")

# Redis cloud
REDIS_DB_NAME = os.environ.get("redis_db_name")
REDIS_ENDPOINT = os.environ.get("redis_db_endpoint")
USERNAME_REDIS = os.environ.get("username_redis")
PASSWORD_REDIS = os.environ.get("password_redis")

# Cloudinary
CLOUDINARY_NAME = os.environ.get("cloud_name")
CLOUDINARY_API = os.environ.get("cloud_api_key")
CLOUDINARY_API_SECRET = os.environ.get("cloud_api_secret")
CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")

# LavinaMQ - analog RebbitMQ
CLUSTER_MQ = os.environ.get("cluster_mq")
HOST_MQ = os.environ.get("host_mq")
USERNAME_MQ = os.environ.get("user_mq")
PASSWORD_MQ = os.environ.get("password_mq")
URL_MQ = os.environ.get("url_mq")
PORT_MQ = os.environ.get("port_mq")
TSL_PORT_MQ = os.environ.get("port_mq_tsl")
