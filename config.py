from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_domain: str
    postgres_port: int

    secret_key: str
    algorithm: str

    expires_delta_access_token: int
    expires_delta_refresh_token: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
