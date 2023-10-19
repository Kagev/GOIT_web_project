import cloudinary
import cloudinary.uploader
from config import settings


class CloudinaryRepository:
	cloud_name = settings.cloudinary_name
	api_key = settings.cloudinary_api
	api_secret = settings.cloudinary_api_secret
	cloud_url = settings.cloudinary_url

	def __init__(self, cloud_name, api_key, api_secret):
		"""

		:type api_secret: object
		:type api_key: object
		:type cloud_name: object
		"""
		cloudinary.config(
			cloud_name=cloud_name,
			api_key=api_key,
			api_secret=api_secret,
		)

	def upload_image(self, image_file):
		"""

		:rtype: object
		"""
		response = cloudinary.uploader.upload(image_file)
		return response

	def get_image_url(self, public_id, format=None) -> object:
		"""

		:rtype: object
		"""
		url, options = cloudinary.utils.cloudinary_url(public_id, format=format, width=100, height=150, crop="fill")
		return {"url": url, "options": options}
