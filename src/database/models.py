from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    photo_id = Column(Integer, ForeignKey('photos.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    user = relationship('User', back_populates='comments')
    photo = relationship('Photo', back_populates='comments')


engine = create_engine('sqlite:///photoshare.db')
Base.metadata.create_all(bind=engine)
