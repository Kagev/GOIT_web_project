from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.services.qr_code import generate_qr_code

router = APIRouter(prefix="/qr_code", tags=["qr_code"])


@router.post("/qr_code")
def create_qr_code(image_url: str = None):
    """Generates a QR code for an image.

    Args:
        image_url: str: The URL of the image.
        db: Session: The database session.

    Returns:
        QRImageResource: The QR image resource object.
    """

    if image_url is None:
        return {"message": "Image URL is required"}

    qr_image_resource = generate_qr_code(image_url)
    return {
        "message": "QR code created successfully",
        "qr_image_resource": qr_image_resource,
    }