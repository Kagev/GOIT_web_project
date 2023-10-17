from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from connection import DATABASE_URL

# DATABASE_URL = URL_DB

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
    with engine.connect() as conn:
        result = conn.execute(query, params)
        return [dict(row) for row in result]

