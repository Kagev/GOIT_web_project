import io
import unittest
from unittest.mock import patch, Mock

from src.services.cloudinary import upload_image

from config import settings


class TestServiceCloudinary(unittest.TestCase):
    @patch('src.services.cloudinary.upload')
    @patch('src.services.cloudinary.cloudinary.CloudinaryImage.build_url')
    @patch('src.services.cloudinary.resource')
    def test_upload_image(self, mock_resource, mock_build_url, mock_upload):
        mock_resource.return_value = {'version': '1234'}
        mock_build_url.return_value = 'https://cloudinary.com/image.jpg'
        mock_upload.return_value = Mock()

        test_file = io.BytesIO(b'test')
        result = upload_image(
            file=test_file,
            user_id=1,
        )

        public_id = settings.cloudinary_folder + 'avatar_1'

        mock_upload.assert_called_once_with(test_file, public_id=public_id, owerwrite=True)
        mock_resource.assert_called_once_with(public_id)
        mock_build_url.assert_called_once_with(width=250, height=250, crop='fill', version='1234')
        self.assertEqual(result, 'https://cloudinary.com/image.jpg')


if __name__ == '__main__':
    unittest.main()
