import asyncio

import pytest
from pytest import mark
from fastapi import status
from sqlalchemy import select

from src.database.models import User
from src.services.auth import auth_service


class TestSignup:
    url_path = "api/auth/signup"

    def test_signup_was_successfully(self, client, user, mocker):
        mocker.patch('src.routes.auth.send_email_confirmed')

        response = client.post(self.url_path, json=user)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["user"]["email"] == user["email"]
        assert response.json()["detail"] == "User successfully created"

    def test_signup_already_existing_email(self, client, user, mocker):
        mocker.patch('src.routes.auth.send_email_confirmed')
        # Test a user creation request with an already existing email
        user = user.copy()
        user['username'] = "test_user2"
        user['password'] = "test_pwd2"

        response = client.post(self.url_path, json=user)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Account already exists"


class TestLogin:
    url_path = "api/auth/login"

    @mark.parametrize(
        "status_code, detail, username, password",
        (
                (status.HTTP_401_UNAUTHORIZED, "Invalid email", "invalid@test.com", None),
                (status.HTTP_401_UNAUTHORIZED, "Email not confirmed", None, None),
                (status.HTTP_401_UNAUTHORIZED, "Invalid password", None, "invalid_pwd"),
        ),
    )
    def test_login_exceptions(self, client, session, user,
                              status_code, detail, username, password):
        if password:
            db_user = session.scalar(select(User).filter(User.email == user['email']))
            db_user.confirmed = True
            session.commit()

        login_data = {
            "username": username or user['email'],
            "password": password or user['password']
        }
        response = client.post(self.url_path, data=login_data)

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    def test_login_was_successfully(self, client, user):
        # Test a valid user login request
        login_data = {"username": user['email'], "password": user['password']}
        response = client.post(self.url_path, data=login_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access_token"] is not None
        assert response.json()["refresh_token"] is not None


class TestRefreshToken:
    url_path = "api/auth/refresh_token"

    def test_refresh_token_was_successfully(self, client, session, user):
        # Test a valid token refresh request
        db_user = session.scalar(select(User).filter(User.email == user['email']))

        headers = {"Authorization": f"Bearer {db_user.refresh_token}"}
        response = client.get(self.url_path, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access_token"] is not None
        assert response.json()["refresh_token"] is not None

    def test_refresh_token_invalid_token(self, client, user):
        # Test a token refresh request with an invalid refresh
        invalid_refresh_token = asyncio.run(
            auth_service.create_refresh_token(data={"sub": user['email']}, expires_delta=100)
        )
        headers = {"Authorization": f"Bearer {invalid_refresh_token}"}
        response = client.get(self.url_path, headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Invalid refresh token"


class TestConfirmedEmail:
    url_path = "api/auth/confirmed_email/{token}"

    def test_confirmed_email_invalid_email(self, client):
        invalid_email_token = asyncio.run(
            auth_service.create_email_token(data={"sub": "invalid@test.com"})
        )
        response = client.get(self.url_path.format(token=invalid_email_token))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['detail'] == "Verification error"

    @mark.parametrize(
        "detail, is_confirmed",
        (
                ("Your email is already confirmed", False),
                ("Email confirmed", True),
        ),
    )
    def test_confirmed_email_was_successfully(self, client, session, user,
                                              detail, is_confirmed):
        if is_confirmed:
            db_user = session.scalar(select(User).filter(User.email == user['email']))
            db_user.confirmed = False
            session.commit()

        email_token = asyncio.run(
            auth_service.create_email_token(data={"sub": user['email']})
        )
        response = client.get(self.url_path.format(token=email_token))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == detail


class TestResetPassword:
    url_path = "api/auth/reset_password"

    @mark.usefixtures('mock_rate_limit')
    def test_reset_password_invalid_email(self, client):
        response = client.post(self.url_path, json={"email": "invalid@test.com"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == "Invalid email"

    @mark.usefixtures('mock_rate_limit')
    def test_reset_password_was_successfully(self, client, user, mocker):
        mocker.patch('src.routes.auth.send_email_reset_password')

        response = client.post(self.url_path, json={"email": user['email']})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "Password reset email sent"


class TestResetPasswordTemplate:
    url_path = "api/auth/reset_password/{token}"

    @mark.parametrize(
        "status_code, detail, email",
        (
                (status.HTTP_400_BAD_REQUEST, "Verification error", "invalid@test.com"),
                (status.HTTP_401_UNAUTHORIZED, "Email not confirmed", None),
        ),
    )
    def test_reset_password_exceptions(self, client, session, user,
                                       status_code, detail, email):
        if not email:
            db_user = session.scalar(select(User).filter(User.email == user['email']))
            db_user.confirmed = False
            session.commit()

        email_token = asyncio.run(
            auth_service.create_email_token(data={"sub": email or user['email']})
        )
        response = client.get(self.url_path.format(token=email_token))

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    def test_reset_password_template_was_successfully(self, client, session, user):
        db_user = session.scalar(select(User).filter(User.email == user['email']))
        db_user.confirmed = True
        session.commit()

        email_token = asyncio.run(
            auth_service.create_email_token(data={"sub": user['email']})
        )
        response = client.get(self.url_path.format(token=email_token))

        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-type'].startswith("text/html")


class TestNewPassword:
    url_path = "api/auth/reset_password/{token}"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    @mark.parametrize(
        "status_code, detail, email",
        (
                (status.HTTP_400_BAD_REQUEST, "Verification error", "invalid@test.com"),
                (status.HTTP_401_UNAUTHORIZED, "Email not confirmed", None),
        ),
    )
    def test_new_password_exceptions(self, client, session, user, status_code, detail, email):
        if not email:
            db_user = session.scalar(select(User).filter(User.email == user['email']))
            db_user.confirmed = False
            session.commit()

        email_token = asyncio.run(
            auth_service.create_email_token(data={"sub": email or user['email']})
        )
        response = client.post(
            self.url_path.format(token=email_token),
            data={"password": user['password']},
            headers=self.headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    def test_new_password_was_successfully(self, client, session, user):
        db_user = session.scalar(select(User).filter(User.email == user['email']))
        db_user.confirmed = True
        session.commit()

        user.update(password="new_pwd")

        email_token = asyncio.run(
            auth_service.create_email_token(data={"sub": user['email']})
        )
        response = client.post(
            self.url_path.format(token=email_token),
            data={"password": user['password']},
            headers=self.headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['status'] == "ok"
