from datetime import datetime, timedelta

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from config import settings
from src.database.models import TokenBL


async def add_token_to_blacklist(email: str, token: str, db: Session) -> bool:
    """
    The function adding token in blacklist in the database.
        It takes email from access token, token itself and add them into blacklist. Return True when it's done.

    :param email: str: User email.
    :param token: str: User access token.
    :param db: Session: Get the database session
    :return: True if it successful.
    :doc-author: yarmel
    """
    tokens_table = TokenBL()
    tokens_table.email = email
    tokens_table.token = token
    db.add(tokens_table)
    db.commit()
    return True


async def is_token_blacklisted(token: str, db: Session) -> bool:
    """
    The function checking if token exists in database blacklist.
        It takes token from user and try to find it in database, return True if successful.

    :param token: str: User access token.
    :param db: Session: Get the database session
    :return: True if it successful.
    :doc-author: yarmel
    """
    if db.execute(select(TokenBL).filter(TokenBL.token == token)).scalar():
        return True


async def clear_expires_records(db: Session):
    """
    The function checking if token exists in database blacklist.
        Just clear expires access tokens from blacklist in database.

    :param db: Session: Get the database session
    :return: None.
    :doc-author: yarmel
    """
    expired_time = datetime.utcnow() - timedelta(minutes=settings.expires_delta_access_token)
    db.execute(delete(TokenBL).where(TokenBL.added_at < expired_time))
    db.commit()
