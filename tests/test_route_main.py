from fastapi import status


def test_root(client):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "REST APP v1.2"


def test_healthchecker(client):
    response = client.get("/api/healthchecker")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Welcome to FastAPI!"
