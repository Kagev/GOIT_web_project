import unittest
from src.database.models import User, Image
from src.repository.image import create_image, get_image, change_description, delte_image_by_id
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from io import BytesIO


class TestImage(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_image(self):
        #создание тестовх данных
        user_id = 1
        description = 'Test image'
        tags = ['tags1', 'tags2']
        file = BytesIO(b'Test image')

        # Вызов тестируемой функции
        image =await create_image(file, user_id, description, tags, db=self.session)

        #Проверка результатов
        self.assertEqual(image.user_id, user_id)
        self.assertEqual(image.description, description)
        self.assertEqual(len(image.tags), 2)
        for tag in image.tags:
            self.assertIn(tag.name, tags)

    async def test_get_image(self):
        #создание тестовх данных
        user_id = 1
        description = 'Test image'
        tags = ['tags1', 'tags2']
        file = BytesIO(b'Test image')

        # Создание изображения в базе данных
        image =await create_image(file, user_id, description, tags, db=self.session)
        image_id = image.id

        # Вызов тестируемой функции
        result =await get_image(image_id, user_id, db=self.session)

        # Проверка результатов
        self.assertEqual(result, image)

    async def test_change_description(self):
        # Создание тестовых данных
        user_id = 1
        description = "Test image"
        tags = ["tag1", "tag2"]
        file = BytesIO(b'Test image content')

        # Создание изображения в базе данных
        image =await create_image(file, user_id, description, tags, db=self.session)
        image_id = image.id

        # Новое описание
        new_description = "New description"

        # Вызов тестируемой функции
        result =await change_description(image_id, user_id, new_description, db=self.session)

        # Проверка результатов
        self.assertEqual(result.description, new_description)

    async def delte_image_by_id(self):
        # Создание тестовых данных
        user_id = 1
        description = "Test image"
        tags = ["tag1", "tag2"]
        file = BytesIO(b'Test image content')

        # Создание изображения в базе данных
        image =await create_image(file, user_id, description, tags, db=self.session)
        image_id = image.id

        # Вызов тестируемой функции
        result =await delte_image_by_id(image_id, user_id, self.session)

        # Проверка результатов
        self.assertEqual(result, True)
        self.assertIsNone(self.session.query(Image).filter(Image.id == image_id).first())


if __name__ == '__main__':
    unittest.main()
