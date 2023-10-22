import io
import uuid
import segno
import cloudinary.uploader
import cloudinary
from config import settings
from src.schemas.qr_schemas import QRImageSchema, QRCodeSchema
from datetime import datetime
from src.database.connection import get_db

cloudinary.config(
	cloud_name=settings.cloudinary_name,
	api_key=settings.cloudinary_api,
	api_secret=settings.cloudinary_api_secret,
	secure=True,
	cloud_folder=settings.cloudinary_folder,
)


def generate_qr_code(image_url: str):
	"""Генерирует QR-код для изображения.

	Args:
		image_url: str: URL изображения.

	Returns:
		QRImageResource: Объект ресурса QR-кода.
	"""

	qr = segno.make(image_url)
	qr_code_path = f"static/qr_codes/qr_{uuid.uuid4()}.png"
	out = io.BytesIO()
	qr.save(qr_code_path, kind='png', scale=4, dark='darkblue', data_dark='#474747', light='#efefef')
	uploaded = cloudinary.uploader.upload(qr_code_path)
	return uploaded["url"]


def save_qr_code(image_url: str, qr_code_url: str):
	"""Сохраняет ссылку на QR-код в базе данных.

	Args:
		image_url: str: URL изображения.
		qr_code_url: str: URL QR-кода в Cloudinary.
	"""

	qr_image_resource = QRCodeSchema(
		image_url=image_url,
		url=qr_code_url,
		created_at=datetime.now(),
	)

	with get_db() as db:
		db.add(qr_image_resource)
		db.commit()


	qr_code_url = generate_qr_code(image_url)
	save_qr_code(image_url, qr_code_url)

	qr_code_url = generate_qr_code(image_url)
	save_qr_code(image_url, qr_code_url, db)
