import pytest
from fastapi.testclient import TestClient
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import app
from src.database.models import Base
from src.database.db import get_db
from src.services.auth import auth_service

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def session() -> Session:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session) -> TestClient:
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="package")
def user() -> dict:
    return {"email": "email@test.com", "username": "test_user", "password": "test_pwd"}


@pytest.fixture(scope="function")
def mock_rate_limit(mocker):
    mock_rate_limit = mocker.patch.object(RateLimiter, '__call__', autospec=True)
    mock_rate_limit.return_value = False


@pytest.fixture(autouse=True)
def mock_auth_redis(mocker):
    mock_redis = mocker.patch.object(auth_service, 'redis', autospec=True)
    mock_redis.get.return_value = None
