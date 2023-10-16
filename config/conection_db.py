import psycopg2
from config.conection_config import *
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = f"postgresql://{POSTGRES_DB_NAME}:{PASSWORD_DB}@{POSTGRES_HOST}:{POSTGRES_PORT}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# Функция для выполнения SQL-запросов с возможностью получения результатов как словарей
def execute_query(query, params=None):
	conn = psycopg2.connect(
		database=POSTGRES_DB_NAME,
		user=USERNAME_DB,
		password=PASSWORD_DB,
		host=URL_DB
	)
	cursor = conn.cursor(cursor_factory=RealDictCursor)
	cursor.execute(query, params)
	result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result
