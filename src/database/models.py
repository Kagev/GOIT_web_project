from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import (
	Column,
	Integer,
	String,
	func,
	DateTime,
	ForeignKey,
	Text,
)


Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String(128), nullable=False)
	email = Column(String(128), nullable=False, unique=True)
	password = Column(String(128), nullable=False)
	created_at = Column(DateTime, default=func.now())
	role = Column(String(64), nullable=False, default="user")
	refresh_token = Column(String(256), nullable=True)

	comments = relationship('Comment', back_populates='users')


class Image(Base):
	__tablename__ = "images"

	id = Column(Integer, primary_key=True, index=True)
	image_name = Column(String, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	path = Column(String, nullable=False)
	description = Column(String, nullable=True)
	created_at = Column(DateTime, default=func.now())
	qr_code = Column(Text)
	tags = relationship("Tag", secondary="image_tags", back_populates="images")
	comments = relationship('Comment', back_populates='images')


class Tag(Base):
	__tablename__ = "tags"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)
	images = relationship("Image", secondary="image_tags", back_populates="tags")


class ImageTagAssociation(Base):
	__tablename__ = "image_tags"

	image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
	tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class Comment(Base):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True, index=True)
	content = Column(String(255), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	image_id = Column(Integer, ForeignKey('images.id'), nullable=False)
	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now())

	users = relationship('User', back_populates='comments')
	images = relationship('Image', back_populates='comments')


class TokenBL(Base):
	__tablename__ = "blacklist"

	id = Column(Integer, primary_key=True)
	email = Column(String(128), nullable=True)
	token = Column(String, nullable=True)
	added_at = Column("added_at", DateTime, default=func.now())
