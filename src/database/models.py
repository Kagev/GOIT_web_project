from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from src.database.connection import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    role = Column(String(64), nullable=False, default="user")
    created_at = Column("created_at", DateTime, default=func.now())
    refresh_token = Column(String(256), nullable=True)


class TokenBL(Base):
    __tablename__ = "blacklist"
    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=True)
    token = Column(String(1024), nullable=True)
    added_at = Column("added_at", DateTime, default=func.now())
