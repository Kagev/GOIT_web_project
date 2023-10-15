import unittest
from unittest.mock import MagicMock
from datetime import timedelta, date

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.shemas.contacts import ContactModel, ContactUpdateModel, ContactPartialUpdateModel
from src.repository.contacts import (
    get_contacts,
    get_contacts_birthdays,
    get_contact_by_id,
    get_contact_by_email,
    create_contact,
    remove_contact,
    update_contact,
    partial_update_contact,
)


class TestRepozitoryContacts(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contact = dict(first_name="Stepan", last_name="Bogdaniv", email='email@example.com',
                           phone_number="380973458623", birth_date=date(1995, 5, 13),
                           additional_data=None)

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_contact(self):
        body = ContactModel(**self.contact)

        result = await create_contact(user=self.user, body=body, db=self.session)

        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.birth_date, body.birth_date)
        self.assertEqual(result.additional_data, body.additional_data)
        self.assertEqual(result.user, self.user)
        self.assertTrue(hasattr(result, "id"))

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.execute.return_value.scalars.return_value.all.return_value = contacts

        result = await get_contacts(user=self.user, skip=0, limit=10,
                                    first_name=None, last_name=None, email=None, db=self.session)  # noqa
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id_found(self):
        mock_contact = Contact(**self.contact)
        self.session.scalar.return_value = mock_contact

        result = await get_contact_by_id(user=self.user, contact_id=1, db=self.session)

        self.assertEqual(result, mock_contact)

    async def test_get_contact_by_id_not_found(self):
        self.session.scalar.return_value = None

        result = await get_contact_by_id(user=self.user, contact_id=1, db=self.session)

        self.assertIsNone(result)

    async def test_get_contact_by_email_found(self):
        mock_contact = Contact(**self.contact)
        self.session.scalar.return_value = mock_contact

        result = await get_contact_by_email(user=self.user, email=self.contact['email'], db=self.session)

        self.assertEqual(result, mock_contact)

    async def test_get_contact_by_email_not_found(self):
        self.session.scalar.return_value = None

        result = await get_contact_by_email(user=self.user, email=self.contact['email'], db=self.session)

        self.assertIsNone(result)

    async def test_get_contacts_birthdays(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.execute.return_value.scalars.return_value.all.return_value = contacts
        result = await get_contacts_birthdays(user=self.user,
                                              from_date=date.today(),
                                              to_date=date.today() + timedelta(weeks=1),
                                              db=self.session)
        self.assertEqual(result, contacts)

    async def test_remove_contact_found(self):
        mock_contact = Contact(**self.contact)
        self.session.scalar.return_value = mock_contact

        result = await remove_contact(user=self.user, contact_id=1, db=self.session)
        self.assertEqual(result, mock_contact)

    async def test_remove_contact_not_found(self):
        self.session.scalar.return_value = None

        result = await remove_contact(user=self.user, contact_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        mock_contact = Contact(**self.contact)
        self.session.execute.return_value.scalar.return_value = mock_contact
        self.session.commit.return_value = None

        result = await update_contact(user=self.user, contact_id=1,
                                      body=ContactUpdateModel(**self.contact), db=self.session)
        self.assertEqual(result, mock_contact)

    async def test_update_contact_not_found(self):
        self.session.execute.return_value.scalar.return_value = None
        self.session.commit.return_value = None

        result = await update_contact(user=self.user, contact_id=1,
                                      body=ContactUpdateModel(**self.contact), db=self.session)
        self.assertIsNone(result)

    async def test_partial_update_contact_found(self):
        mock_contact = Contact(**self.contact)
        self.session.execute.return_value.scalar.return_value = mock_contact
        self.session.commit.return_value = None

        result = await partial_update_contact(user=self.user, contact_id=1,
                                              body=ContactPartialUpdateModel(**self.contact), db=self.session)
        self.assertEqual(result, mock_contact)

    async def test_partial_update_contact_not_found(self):
        self.session.execute.return_value.scalar.return_value = None
        self.session.commit.return_value = None

        result = await partial_update_contact(user=self.user, contact_id=1,
                                              body=ContactPartialUpdateModel(**self.contact), db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
