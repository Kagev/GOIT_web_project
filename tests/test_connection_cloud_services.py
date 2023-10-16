import unittest
import psycopg2
import redis
import pika
from cloudinary import CloudinaryImage
from config.conection_config import *
from config.conection_db import DATABASE_URL


class TestCloudServicesConnection(unittest.TestCase):
	def test_redis_connection(self):
		try:
			import redis

			r = redis.Redis(
				host=REDIS_DB_HOST,
				port=REDIS_DB_PORT,
				password=PASSWORD_REDIS)
			r.ping()
			print("Redis connection successful!")
		except Exception as e:
			print("Error connecting to Redis:", str(e))

	def test_elephant_sql_connection(self):
		try:
			conn = psycopg2.connect(url=DATABASE_URL)
			print("ElephantSQL connection successful!")
			conn.close()
		except Exception as e:
			print("Error connecting to ElephantSQL:", str(e))

	def test_lavina_mq_connection(self):
		try:
			credentials = pika.PlainCredentials(USERNAME_MQ, PASSWORD_MQ)
			parameters = pika.ConnectionParameters(HOST_MQ, PORT_MQ, '/', credentials)
			connection = pika.BlockingConnection(parameters)
			channel = connection.channel()
			print("LavinaMQ connection successful!")
			connection.close()
		except Exception as e:
			print("Error connecting to LavinaMQ:", str(e))

	def test_cloudinary_connection(self):
		try:
			cloudinary_url = CLOUDINARY_URL
			img = CloudinaryImage("sample").build_url(width=100, height=100, crop='fill')
			print("Cloudinary connection successful!")
			print(f"Sample image URL: {img}")
		except Exception as e:
			print("Error connecting to Cloudinary:", str(e))


if __name__ == '__main__':
	unittest.main()
