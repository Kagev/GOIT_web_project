from datetime import datetime, timedelta

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from src.database.models import TokenBL
from config import settings


async def add_token_to_blacklist(email: str, token: str, db: Session) -> bool:
    tokens_table = TokenBL()
    tokens_table.email = email
    tokens_table.token = token
    db.add(tokens_table)
    db.commit()
    return True


async def is_token_blacklisted(token: str, db: Session) -> bool:
    if db.execute(select(TokenBL).filter(TokenBL.token == token)).scalar():
        return True


async def clear_expires_records(db: Session):
    expired_time = datetime.utcnow() - timedelta(minutes=settings.expires_delta_access_token)
    db.execute(delete(TokenBL).where(TokenBL.added_at < expired_time))
    db.commit()
