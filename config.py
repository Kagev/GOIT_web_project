from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB block
    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_domain: str
    postgres_port: int

    # # REDIS block
    # redis_host: str
    # redis_port: int
    #
    # # Mail block
    # mail_username: str
    # mail_password: str
    # mail_from: str
    # mail_port: int
    # mail_server: str
    #
    # # Cloudinary block
    # cloudinary_name: str
    # cloudinary_api_key: int
    # cloudinary_api_secret: str
    # cloudinary_folder: str = "PyCrafters/"

    # Token block
    secret_key: str
    algorithm: str
    expires_delta_access_token: int
    expires_delta_refresh_token: int

    # Users block
    allowed_roles: list = ["user", "moderator", "admin"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
