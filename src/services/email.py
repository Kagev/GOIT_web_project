from pydantic import EmailStr
from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from fastapi_mail.errors import ConnectionErrors

from .auth import auth_service
from config import settings, Template


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Template.emails,
)


async def send_email_reset_password(email: EmailStr, username: str, host: str):
    try:
        token_verification = await auth_service.create_email_token({"sub": email})

        message = MessageSchema(
            subject="Reset password ",
            recipients=[email],
            template_body={"host": host, "full_name": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password.html")
    except ConnectionErrors as err:
        print(err)


async def send_email_confirmed(email: EmailStr, username: str, host: str) -> None:
    try:
        token_verification = await auth_service.create_email_token({"sub": email})

        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="confirmed_email.html")
    except ConnectionErrors as err:
        print(err)
