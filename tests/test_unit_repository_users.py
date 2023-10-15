import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.models import User
from src.shemas.users import UserModel
from src.repository.users import (
    create_user,
    confirmed_email,
    get_user_by_id,
    get_user_by_email,
    update_token,
    update_avatar,
    update_email,
    update_password,
)


class TestRepositoryUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.body = UserModel(
            username="username",
            email="email@example.com",
            password="qwerty_123",
        )

    async def test_create_user(self):
        with patch.object(Gravatar, 'get_image', return_value="https://www.gravatar.com/avatar/test_image") as mock_get_image:

            result = await create_user(self.body, self.session)

            mock_get_image.assert_called_once_with()
            self.assertIsInstance(result, User)
            self.assertEqual(result.username, self.body.username)
            self.assertEqual(result.email, self.body.email)
            self.assertEqual(result.password, self.body.password)
            self.assertEqual(result.avatar, "https://www.gravatar.com/avatar/test_image")
            self.assertTrue(hasattr(result, 'id'))

            self.session.add.assert_called_once_with(result)
            self.session.commit.assert_called_once()
            self.session.refresh.assert_called_once_with(result)

    async def test_confirmed_email(self):
        user = User(id=1)

        result = await confirmed_email(user, self.session)

        self.assertIsNone(result)
        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()

    async def test_get_user_by_id_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await get_user_by_id(user_id=1, db=self.session)

        self.assertEqual(result, mock_user)

    async def test_get_user_by_id_not_found(self):
        self.session.execute.return_value.scalar.return_value = None

        result = await get_user_by_id(user_id=1, db=self.session)

        self.assertIsNone(result)

    async def test_get_user_by_email_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await get_user_by_email(email="email@example.com", db=self.session)

        self.assertEqual(result, mock_user)

    async def test_get_user_by_email_not_found(self):
        self.session.execute.return_value.scalar.return_value = None

        result = await get_user_by_email(email="email@example.com", db=self.session)

        self.assertIsNone(result)

    async def test_update_token_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        new_token = "new_token"
        result = await update_token(user=mock_user, token=new_token, db=self.session)

        self.assertIsNone(result)
        self.assertEqual(mock_user.refresh_token, new_token)
        self.session.commit.assert_called_once()

    async def test_update_avatar_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await update_avatar(user_id=1, url="new_avatar_url", db=self.session)

        self.assertEqual(result, mock_user)
        self.session.commit.assert_called_once()

    async def test_update_email_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await update_email(user_id=1, email="email@example.com", db=self.session)

        self.assertEqual(result, mock_user)
        self.session.commit.assert_called_once()

    async def test_update_password_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await update_password(user_id=1, password="new_password", db=self.session)

        self.assertEqual(result, mock_user)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
