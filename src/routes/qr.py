from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.services import qr as qr_services
from src.database.models import User
from src.services.auth import auth_service

router = APIRouter(prefix="/qr", tags=["qr"])
templates = Jinja2Templates(directory="src/templates/qr")


@router.post("/generate/", response_class=HTMLResponse)
async def generate_qr_code(
    image_url: str,
    request: Request,
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The generate_qr_code generate a html page with QR-code with image url.
        Only for authenticated users.

        :param image_url: str: url to image for code generation.
        :param request: Request: request for incoming HTTP connections.
        :param current_user: User: Get the current user from the auth_service.
        :return: HTML page with generated QR-code.
        :doc-author: yarmel
    """
    if current_user:
        qr_code = await qr_services.generate_qr_code(image_url)
        qr_image = await qr_services.generate_qr_url(qr_code)
        return templates.TemplateResponse(
            "result.html", {"request": request, "qr_image": qr_image}
        )
