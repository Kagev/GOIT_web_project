import qrcode
from qrcode.image.base import BaseImage
from io import BytesIO
from base64 import b64encode


async def generate_qr_code(image_url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(image_url)
    qr.make(fit=True)

    qr_code = qr.make_image(fill_color="black", back_color="white")

    return qr_code


async def generate_qr_url(qr_code: BaseImage):
    image_io = BytesIO()
    qr_code.save(image_io, 'PNG')
    data_url = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
    return data_url
