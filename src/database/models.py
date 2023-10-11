from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(Base):
	__tablename__ = "user_roles"
	id = Column(Integer, primary_key=True, index=True)
	role_name = Column(String(50), unique=True, nullable=False)


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(50), unique=True, nullable=False)
	email = Column(String(250), unique=True, nullable=False)
	password = Column(String(255), nullable=False)
	created_at: Column(DateTime, default=func.now())
	avatar: Column(String(255))
	refresh_token: Column(String(255))
	confirmed: Column(default=False)
	role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
	role = relationship("UserRole", back_populates="users")


class Photo(Base):
	__tablename__ = "photos"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	description = Column(String(255))
	tags = Column(String(255))
	created_at = Column(DateTime, default=func.now())

	user = relationship("User", back_populates="photos")
	comments = relationship("Comment", back_populates="photo")


class Comment(Base):
	__tablename__ = "comments"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)
	content = Column(String(255))
	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, onupdate=func.now())

	user = relationship("User", back_populates="comments")
	photo = relationship("Photo", back_populates="comments")


engine = create_engine("sqlite:///photoshare.db")
Base.metadata.create_all(bind=engine)
