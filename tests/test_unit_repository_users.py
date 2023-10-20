import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.users import UserModel, UserProfileUpdate
from src.repository import users as users_repository


class TestRepositoryUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.test_user = User(
            username="username",
            email="email@example.com",
        )
        self.user_model_body = UserModel(
            username="username",
            email="email@example.com",
            password="qwerty_123",
        )
        self.user_profile_update_body = UserProfileUpdate(
            username="username",
            email="email@example.com",
        )

    async def test_create_user(self):

        result = await users_repository.create_user(self.user_model_body, self.session)

        self.assertIsInstance(result, User)
        self.assertEqual(result.username, self.user_model_body.username)
        self.assertEqual(result.email, self.user_model_body.email)
        self.assertEqual(result.password, self.user_model_body.password)
        self.assertTrue(hasattr(result, 'id'))

        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

    async def test_users_count(self):
        self.session.execute.return_value.scalar.return_value = 1

        result = await users_repository.users_count(db=self.session)

        self.assertEqual(result, 1)

    async def test_get_user_by_email_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await users_repository.get_user_by_email(email="email@example.com", db=self.session)

        self.assertEqual(result, mock_user)

    async def test_get_user_by_email_not_found(self):
        self.session.execute.return_value.scalar.return_value = None

        result = await users_repository.get_user_by_email(email="email@example.com", db=self.session)

        self.assertIsNone(result)

    async def test_get_user_by_username_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        result = await users_repository.get_user_by_username(username="username", db=self.session)

        self.assertEqual(result, mock_user)

    async def test_get_user_by_username_not_found(self):
        self.session.execute.return_value.scalar.return_value = None

        result = await users_repository.get_user_by_username(username="username", db=self.session)

        self.assertIsNone(result)

    async def test_update_token_found(self):
        mock_user = User()
        self.session.execute.return_value.scalar.return_value = mock_user

        new_token = "new_token"
        result = await users_repository.update_token(user=mock_user, token=new_token, db=self.session)

        self.assertIsNone(result)
        self.assertEqual(mock_user.refresh_token, new_token)
        self.session.commit.assert_called_once()

    async def test_assign_admin_role(self):
        mock_user = User()
        mock_user.is_admin = False
        self.session.execute.return_value.scalar.return_value = mock_user.is_admin = True

        result = await users_repository.assign_admin_role(mock_user, db=self.session)

        self.assertEqual(result.is_admin, mock_user.is_admin)
        self.session.commit.assert_called_once()

    async def test_remove_admin_role(self):
        mock_user = User()
        mock_user.is_admin = True
        self.session.execute.return_value.scalar.return_value = mock_user.is_admin = False

        result = await users_repository.remove_admin_role(mock_user, db=self.session)

        self.assertEqual(result.is_admin, mock_user.is_admin)
        self.session.commit.assert_called_once()

    async def test_assign_moderator_role(self):
        mock_user = User()
        mock_user.is_moderator = False
        self.session.execute.return_value.scalar.return_value = mock_user.is_moderator = True

        result = await users_repository.assign_moderator_role(mock_user, db=self.session)

        self.assertEqual(result.is_moderator, mock_user.is_moderator)
        self.session.commit.assert_called_once()

    async def test_remove_moderator_role(self):
        mock_user = User()
        mock_user.is_moderator = True
        self.session.execute.return_value.scalar.return_value = mock_user.is_moderator = False

        result = await users_repository.remove_moderator_role(mock_user, db=self.session)

        self.assertEqual(result.is_moderator, mock_user.is_moderator)
        self.session.commit.assert_called_once()

    async def test_edit_user(self):
        self.session.execute.return_value.scalar.return_value = self.test_user

        result = await users_repository.edit_user(username="username", body=self.user_profile_update_body, db=self.session)

        self.assertEqual(result.username, self.user_profile_update_body.username)
        self.assertEqual(result.email, self.user_profile_update_body.email)
        self.session.commit.assert_called_once()

    async def test_add_ban_user(self):
        mock_user = User()
        mock_user.is_banned = False
        self.session.execute.return_value.scalar.return_value = mock_user.is_banned = True

        result = await users_repository.add_ban_user(mock_user, db=self.session)

        self.assertEqual(result.is_moderator, mock_user.is_moderator)
        self.session.commit.assert_called_once()

    async def test_remove_ban_user(self):
        mock_user = User()
        mock_user.is_banned = True
        self.session.execute.return_value.scalar.return_value = mock_user.is_banned = False

        result = await users_repository.remove_ban_user(mock_user, db=self.session)

        self.assertEqual(result.is_banned, mock_user.is_banned)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
