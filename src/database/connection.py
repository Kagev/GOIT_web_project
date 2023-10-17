from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import settings

user = settings.postgres_user
password = settings.postgres_password
db_name = settings.postgres_name
domain = settings.postgres_domain
port = settings.postgres_port

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{domain}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)


def get_db():
    db = Session(engine)
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    finally:
        db.close()
