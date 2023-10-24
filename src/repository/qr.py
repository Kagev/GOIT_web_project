from src.database.connection import get_db
from src.schemas.qr import QRCodeSchema, QRImageSchema
from datetime import datetime

from src.services.qr import generate_qr_code


def save_qr_code_url(image_url: str, qr_code_url: str):
    """Сохраняет ссылку на QR-код в базе данных.

    Args:
            image_url: str: URL изображения.
            qr_code_url: str: URL QR-кода в Cloudinary.
    """

    qr_image_resource = QRImageSchema(
        image_url=image_url,
        url=qr_code_url,
        created_at=datetime.now(),
    )

    with get_db() as db:
        db.add(qr_image_resource)
        db.commit()

    qr_code_url = generate_qr_code(image_url)
    save_qr_code_url(image_url, qr_code_url)
