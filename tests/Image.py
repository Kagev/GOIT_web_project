import unittest
from src.database.models import Tag, Photo, User
from src.repository.image import create_image, get_image, delete_image, change_description
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from io import BytesIO


class TestImage(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    def test_create_image(self):
        #создание тестовх данных
        user_id = 1
        description = 'Test image'
        tags = ['tags1', 'tags2']
        file = BytesIO(b'Test image')

        # Вызов тестируемой функции
        image = create_image(file, user_id, description, tags, self.session)

        #Проверка результатов
        self.assertEqual(image.user_id, user_id)
        self.assertEqual(image.description, description)
        self.assertEqual(len(image.tags), 2)
        for tag in image.tags:
            self.assertIn(tag.name, tags)

    def test_get_image(self):
        #создание тестовх данных
        user_id = 1
        description = 'Test image'
        tags = ['tags1', 'tags2']
        file = BytesIO(b'Test image')

        # Создание изображения в базе данных
        image = create_image(file, user_id, description, tags, self.session)
        image_id = image.id

        # Вызов тестируемой функции
        result = get_image(image_id, user_id, self.session)

        # Проверка результатов
        self.assertEqual(result, image)

    def test_change_description(self):
        # Создание тестовых данных
        user_id = 1
        description = "Test image"
        tags = ["tag1", "tag2"]
        file = BytesIO(b'Test image content')

        # Создание изображения в базе данных
        image = create_image(file, user_id, description, tags, self.session)
        image_id = image.id

        # Новое описание
        new_description = "New description"

        # Вызов тестируемой функции
        result = change_description(image_id, user_id, new_description, self.session)

        # Проверка результатов
        self.assertEqual(result.description, new_description)

    def test_delete_image(self):
        # Создание тестовых данных
        user_id = 1
        description = "Test image"
        tags = ["tag1", "tag2"]
        file = BytesIO(b'Test image content')

        # Создание изображения в базе данных
        image = create_image(file, user_id, description, tags, self.session)
        image_id = image.id

        # Вызов тестируемой функции
        result = delete_image(image_id, user_id, self.session)

        # Проверка результатов
        self.assertEqual(result, True)
        self.assertIsNone(self.session.query(Photo).filter(Photo.id == image_id).first())


if __name__ == '__main__':
    unittest.main()