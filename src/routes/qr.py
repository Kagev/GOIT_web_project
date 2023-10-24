from fastapi import APIRouter
from src.services.qr import generate_qr_code

router = APIRouter(prefix="/qr", tags=["qr_code"])


@router.post("/generate")
def create_qr_code(image_url: str = None):
    """Generates a QR code for an image.

    Args:
        image_url: str: The URL of the image.

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
