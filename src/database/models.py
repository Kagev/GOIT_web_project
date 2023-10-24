from sqlalchemy import (
	Column,
	Integer,
	String,
	func,
	DateTime,
	ForeignKey,
	Text

)

from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped

Base = declarative_base()


class PrimaryKeyABC:
	__abstract__ = True
	id = Column(Integer, primary_key=True)


class CreatedAtABC:
	__abstract__ = True
	created_at = Column(DateTime, default=func.now())


class UpdatedAtABC:
	__abstract__ = True
	updated_at = Column(DateTime, default=func.now())


class User(Base, PrimaryKeyABC, CreatedAtABC):
	__tablename__ = "users"

	username = Column(String(128), nullable=False, unique=True)
	email = Column(String(128), nullable=False, unique=True)
	about = Column(String(512), nullable=True, default="")
	password = Column(String(128), nullable=False)
	is_admin: Mapped[bool] = mapped_column(default=False)
	is_moderator: Mapped[bool] = mapped_column(default=False)
	is_banned: Mapped[bool] = mapped_column(default=False)
	refresh_token = Column(String(256), nullable=True)

	comments = relationship('Comment', back_populates='users')


class Image(Base, PrimaryKeyABC, CreatedAtABC):
	__tablename__ = "images"

	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	path = Column(String, nullable=False)
	description = Column(String, nullable=True)

	tags = relationship("Tag", secondary="image_tags", back_populates="images")
	comments = relationship('Comment', back_populates='images')


class Tag(Base, PrimaryKeyABC):
	__tablename__ = "tags"

	name = Column(String, unique=True, index=True)

	images = relationship("Image", secondary="image_tags", back_populates="tags")


class ImageTagAssociation(Base):
	__tablename__ = "image_tags"

	image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
	tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class Comment(Base, PrimaryKeyABC, CreatedAtABC, UpdatedAtABC):
	__tablename__ = 'comments'

	content = Column(String(255), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	image_id = Column(Integer, ForeignKey('images.id'), nullable=False)

	users = relationship('User', back_populates='comments')
	images = relationship('Image', back_populates='comments')


class TokenBL(Base, PrimaryKeyABC):
	__tablename__ = "blacklist"

	email = Column(String(128), nullable=True)
	token = Column(String, nullable=True)
	added_at = Column("added_at", DateTime, default=func.now())


class CloudinaryResource(Base, PrimaryKeyABC, CreatedAtABC):
	__tablename__ = "cloudinary_resources"

	public_id = Column(String, nullable=False)
	format = Column(String)
	version = Column(Integer)
	resource_type = Column(String)
	tags = Column(String)
	bytes = Column(Integer)
	width = Column(Integer)
	height = Column(Integer)
	url = Column(String)
	secure_url = Column(String)
	next_cursor = Column(String)
	transformation = Column(String)
	pages = Column(String)


class QRImageResource(Base, PrimaryKeyABC, CreatedAtABC):
	__tablename__ = "qr_image_resources"

	img_transform_url = Column(String(255), nullable=False)
	public_id = Column(String(255), nullable=False)
	qr_code_url = Column(Text, nullable=False)
