"""
Processing our images using the Cloudinary service
"""

from typing import BinaryIO
import cloudinary
from cloudinary.api import resource
from cloudinary.uploader import upload
from config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def upload_image(
    file: BinaryIO, user_id: int, return_size: tuple[int, int] = (250, 250)
) -> str:
    """
    The upload_image function takes a file, uploads it to Cloudinary and returns the URL of the uploaded image.

    :param file: BinaryIO: Pass in the file to be uploaded
    :param user_id: int: Specify the user id of the user who uploaded the image
    :param return_size: tuple[int, int]: Set the width and height of the image
    :return: The url of the uploaded image
    """
    file_id = settings.cloudinary_folder + f"avatar_{user_id}"
    upload(file, public_id=file_id, owerwrite=True)

    return cloudinary.CloudinaryImage(file_id).build_url(
        width=return_size[0],
        height=return_size[1],
        crop="fill",
        version=resource(file_id)["version"],
    )


def transform_img(public_id, width, height, crop):
    """
    The transform_img function takes a Cloudinary public_id and an optional quality parameter to optimize the image.

    :param public_id: str: Public ID of the image to optimize
    :param width: set the image width for cropping
    :param height: set the image height for cropping
    :param crop: a command that crops according to the Height and Width parameters we set
    :return: The returns us images from Cloudinary transformed_url
    """

    # url, options = cloudinary_url("olympic_flag", width=100, height=150, crop="fill")
    # Crete object CloudinaryImage
    image = cloudinary.CloudinaryImage(public_id)

    # Crete object Transformation
    transformation = cloudinary.Transformation()
    transformation.width(width)
    transformation.height(height)
    transformation.crop(crop)

    # Get URL transform image
    transformed_url = image.build_url(transformation=transformation)

    return transformed_url


def optimize_media(public_id, quality=80):
    """
    The optimize_media function takes a Cloudinary public_id and an optional quality parameter to optimize the image.

    :param public_id: str: Public ID of the image to optimize
    :param quality: int: Image quality (0-100), where 0 is the lowest quality and 100 is the highest.
    :return: The response from Cloudinary
    """
    # Set quality for optimization
    update_result = cloudinary.update(public_id, quality=quality)

    return update_result
