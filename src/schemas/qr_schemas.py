from pydantic import BaseModel
from datetime import datetime


class QRCodeSchema(BaseModel):
	qr_code_url: str
	public_id: str
	img_transform_url: str
	created_at: datetime

	class Config:
		from_attributes = True


class QRImageSchema(BaseModel):
	image_url: str
	url: str
	created_at: datetime

	class Config:
		from_attributes = True
