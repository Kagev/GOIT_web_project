from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings


engine = create_engine(settings.db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
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
