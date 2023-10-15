from pytest import fixture, mark
from fastapi import status
from sqlalchemy import select

from src.database.models import User


@fixture()
def access_token(client, user, session, mocker) -> str:
    mocker.patch('src.routes.auth.send_email_confirmed')

    client.post("/api/auth/signup", json=user)

    current_user: User = session.scalar(select(User).filter(User.email == user['email']))
    current_user.confirmed = True
    session.commit()

    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    return response.json()['access_token']


class TestGetMy:
    url_path = "api/users/me"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
        )
    )
    def test_get_me_exceptions(self, client, access_token,
                               status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        else:
            headers = {}

        response = client.get(self.url_path, headers=headers)

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_get_me_was_successfully(self, client, access_token, user):
        response = client.get(
            self.url_path,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['email'] == user['email']


class TestUpdateAvatar:
    url_path = "api/users/avatar"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
        )
    )
    def test_update_avatar_exceptions(self, client, access_token,
                                      status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        else:
            headers = {}

        response = client.patch(
            self.url_path,
            files={"file": ("test.png", b"image", "image/png")},
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_update_avatar_was_successfully(self, client, access_token, user, mocker):
        mock_avatar = "https://res.cloudinary.com/dlwnuqx3p/image/upload/v1678785308/cld-sample-5.jpg"
        mocker.patch("src.services.cloudinary.upload_image", return_value=mock_avatar)

        response = client.patch(
            self.url_path,
            files={"file": ("test.png", b"image", "image/png")},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['email'] == user['email']
        assert response.json()['avatar'] == mock_avatar


class TestUpdateEmail:
    url_path = "api/users/email"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
        )
    )
    def test_update_email_exceptions(self, client, access_token, user,
                                     status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        else:
            headers = {}

        response = client.patch(
            self.url_path,
            json={"email": "update.email@test.com"},
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_update_email_was_successfully(self, client, access_token, user):
        user.update(email="update.email@test.com")

        response = client.patch(
            self.url_path,
            json={"email": user['email']},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['email'] == user['email']


class TestUpdatePassword:
    url_path = "api/users/password"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_401_UNAUTHORIZED, "Invalid old password", "valid"),
        )
    )
    def test_update_password_exceptions(self, client, access_token, user,
                                        status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            headers = {}

        response = client.patch(
            self.url_path,
            json={"old_password": "invalid", "new_password": "update_pwd"},
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_update_password_was_successfully(self, client, access_token, user):
        new_password = "update_pwd"

        response = client.patch(
            self.url_path,
            json={"old_password": user['password'], "new_password": new_password},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        user.update(password=new_password)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['email'] == user['email']
