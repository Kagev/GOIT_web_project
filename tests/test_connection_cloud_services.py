import pytest
from unittest.mock import MagicMock, patch
import psycopg2
import redis
import pika
from cloudinary import CloudinaryImage

from config import settings
from src.database.connection import DATABASE_URL


@pytest.fixture
def mock_redis():
	return redis.Redis(host=settings.REDIS_DB_HOST, port=settings.REDIS_DB_PORT, password=settings.PASSWORD_REDIS)


@pytest.fixture
def mock_pika_connection():
	credentials = pika.PlainCredentials(settings.USERNAME_MQ, settings.PASSWORD_MQ)
	parameters = pika.ConnectionParameters(settings.HOST_MQ, settings.PORT_MQ, '/', credentials)
	return pika.BlockingConnection(parameters)


def test_redis_connection(mock_redis):
	with patch('redis.Redis') as mock_redis:
		mock_redis.return_value.ping.return_value = True
		assert mock_redis().ping()


def test_elephant_sql_connection():
	with patch('psycopg2.connect') as mock_connect:
		mock_connect.return_value = MagicMock()
		assert psycopg2.connect(url=DATABASE_URL)


def test_lavina_mq_connection(mock_pika_connection):
	with patch('pika.BlockingConnection') as mock_pika:
		mock_pika.return_value.channel.return_value = MagicMock()
		assert mock_pika_connection.channel()


def test_cloudinary_connection():
	with patch('cloudinary.CloudinaryImage') as mock_cloudinary:
		mock_build_url = MagicMock()
		mock_cloudinary.return_value.build_url.return_value = mock_build_url
		img = CloudinaryImage("sample").build_url(width=100, height=100, crop='fill')
		assert img is not None
