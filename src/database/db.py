from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database.connection import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Gets local session for database.

    :return: Database session.
    :rtype: Session
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# function for executing SQL queries with the ability to obtain results as dictionaries
def execute_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(query, params)
        return [dict(row) for row in result]

