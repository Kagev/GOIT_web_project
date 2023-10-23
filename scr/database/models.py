from sqlalchemy import Column, Integer, String, Text
from database import Base

class ImageData(Base):
    __tablename__ = 'image_data'

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, index=True)
    qr_code = Column(Text)
