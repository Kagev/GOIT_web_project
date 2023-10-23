from datetime import date

from pytest import mark, fixture
from fastapi import status
from sqlalchemy import select

from src.database.models import User, Contact


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


@fixture(scope="module")
def contact() -> dict:
    return dict(
        first_name='Stepan',
        last_name='Giga',
        email='giga@test.com',
        phone_number='380958765646',
        birth_date=str(date(1970, 10, 13)),
        additional_data=None,
    )


class TestCreateContact:
    url_path = "api/contacts/"

    @mark.usefixtures('mock_rate_limit')
    def test_create_contact_was_successfully(self, client, contact, access_token):
        response = client.post(
            self.url_path,
            json=contact,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('id') is not None
        assert response.json()['email'] == contact['email']

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_409_CONFLICT, "A contact with this email address already exists", "valid"),
        )
    )
    def test_create_contact_exceptions(self, client, access_token, contact,
                                       status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            headers = {}

        response = client.post(self.url_path, json=contact, headers=headers)

        assert response.status_code == status_code
        assert response.json()['detail'] == detail


class TestGetContacts:
    url_path = "api/contacts/"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
        )
    )
    def test_get_contacts_exceptions(self, client, access_token,
                                     status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        else:
            headers = {}

        response = client.get(self.url_path, headers=headers)

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "query_params",
        (
                ({"skip": 0, "limit": 10, "first_name": "Stepan"}),
                ({"skip": 0, "limit": 10, "last_name": "Giga"}),
                ({"skip": 0, "limit": 10, "email": "giga@test.com"}),
                ({"skip": 0, "limit": 10, "email": "invalid@test.com"}),
        )
    )
    def test_get_contacts_successfully(self, client, access_token, contact,
                                       query_params):
        response = client.get(
            self.url_path,
            params=query_params,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

        response_contacts = response.json()

        if query_params.get('email') == "invalid@test.com":
            assert response_contacts == []
        else:
            response_contact = response_contacts[0]

            assert response_contact['email'] == contact['email']
            assert response_contact['first_name'] == contact['first_name']
            assert response_contact['last_name'] == contact['last_name']


class TestGetContactsBirthdays:
    url_path = "api/contacts/birthdays"

    def startup_method(self, session):
        self.mock_contacts = session.scalars(select(Contact)).all()

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_422_UNPROCESSABLE_ENTITY, "The {from_date} parameter cannot be "
                                                       "greater than the {to_date} parameter", "valid"),
        )
    )
    def test_get_contacts_birthdays_exceptions(self, client, access_token, contact,
                                               status_code, detail, authorization):
        data = dict(
            from_date=str(date(2023, 10, 10)),
        )

        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
            data['to_date'] = str(date(2023, 10, 5))
        else:
            headers = {}

        response = client.get(self.url_path, params=data, headers=headers)

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_get_contacts_birthdays_was_successfully(self, client, access_token, contact, mocker, session):
        mocker.patch(
            "src.repository.contacts.get_contacts_birthdays",
            return_value=session.scalars(select(Contact)).all(),
        )

        data = dict(
            from_date=str(date(2023, 10, 10)),
            to_date=str(date(2023, 10, 17)),
        )
        response = client.get(
            self.url_path,
            params=data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

        response_contact = response.json()[0]

        assert response_contact['email'] == contact['email']


class TestGetContact:
    url_path = "api/contacts/{contact_id}"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_404_NOT_FOUND, "Contact not found", "valid"),
        )
    )
    def test_get_contact_exceptions(self, client, access_token,
                                    status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            headers = {}

        response = client.get(
            self.url_path.format(contact_id=0),
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_get_contact_was_successfully(self, client, access_token, contact, session):
        response = client.get(
            self.url_path.format(contact_id=1),
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['email'] == contact['email']


class TestUpdateContact:
    url_path = "api/contacts/{contact_id}"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_404_NOT_FOUND, "Contact not found", "valid"),
        )
    )
    def test_update_contact_exceptions(self, client, access_token, contact,
                                       status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            headers = {}

        response = client.put(
            self.url_path.format(contact_id=0),
            json=contact,
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_update_contact_was_successfully(self, client, access_token, contact, session):
        contact.update(
            first_name='Степан',
            last_name='Гіга',
            email='new.giga@test.com',
            phone_number='380950001221',
            birth_date=str(date(1959, 11, 16)),
            additional_data="New additional data",
        )

        response = client.put(
            self.url_path.format(contact_id=1),
            json=contact,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['first_name'] == contact['first_name']
        assert response.json()['last_name'] == contact['last_name']
        assert response.json()['email'] == contact['email']
        assert response.json()['phone_number'] == contact['phone_number']
        assert response.json()['birth_date'] == contact['birth_date']
        assert response.json()['additional_data'] == contact['additional_data']


class TestPartialUpdateContact:
    url_path = "api/contacts/{contact_id}"

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_404_NOT_FOUND, "Contact not found", "valid"),
        )
    )
    def test_partial_update_contact_exceptions(self, client, access_token, contact,
                                               status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            headers = {}

        response = client.put(
            self.url_path.format(contact_id=0),
            json=contact,
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail

    @mark.usefixtures('mock_rate_limit')
    def test_partial_update_contact_was_successfully(self, client, access_token, contact, session):
        contact.update(
            email='s.giga@test.com',
            phone_number='380950009559',
            additional_data='український естрадний співак, композитор, народний артист України',
        )

        response = client.put(
            self.url_path.format(contact_id=1),
            json=contact,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['first_name'] == contact['first_name']
        assert response.json()['last_name'] == contact['last_name']
        assert response.json()['email'] == contact['email']
        assert response.json()['phone_number'] == contact['phone_number']
        assert response.json()['birth_date'] == contact['birth_date']
        assert response.json()['additional_data'] == contact['additional_data']


class TestRemoveContact:
    url_path = "api/contacts/{contact_id}"

    @mark.usefixtures('mock_rate_limit')
    def test_remove_contact_was_successfully(self, client, access_token, contact, session):
        response = client.delete(
            self.url_path.format(contact_id=1),
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['first_name'] == contact['first_name']
        assert response.json()['last_name'] == contact['last_name']
        assert response.json()['email'] == contact['email']
        assert response.json()['phone_number'] == contact['phone_number']
        assert response.json()['birth_date'] == contact['birth_date']
        assert response.json()['additional_data'] == contact['additional_data']

    @mark.usefixtures('mock_rate_limit')
    @mark.parametrize(
        "status_code, detail, authorization",
        (
                (status.HTTP_401_UNAUTHORIZED, "Not authenticated", None),
                (status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", "invalid"),
                (status.HTTP_404_NOT_FOUND, "Contact not found", "valid"),
        )
    )
    def test_remove_contact_exceptions(self, client, access_token, contact,
                                       status_code, detail, authorization):
        if authorization == "invalid":
            headers = {"Authorization": "Bearer invalid_access_token"}
        elif authorization == "valid":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            headers = {}

        response = client.delete(
            self.url_path.format(contact_id=1),
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()['detail'] == detail
