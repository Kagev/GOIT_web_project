from sqlalchemy import Boolean, Column,DateTime, Integer,ForeignKey, func, String, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config.conection_db import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    birth_date = Column(Date)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String)
    refresh_token = Column(String(255))
    confirmed = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    role = relationship("UserRole", back_populates="users")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    path = Column(String, nullable=False)
    description = Column(String, nullable=True)
    tags = relationship("Tag", secondary="image_tags", back_populates="images")
    created_at = Column(DateTime, default=func.now())


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    images = relationship("Photo", secondary="photo_tags", back_populates="tags")


class PhotoTagAssociation(Base):
    __tablename__ = "photo_tags"

    image_id = Column(Integer, ForeignKey("photos.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
