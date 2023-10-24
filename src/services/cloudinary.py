import uuid
from typing import BinaryIO
import cloudinary
from cloudinary.api import resource
from cloudinary.uploader import upload
from config import settings


cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
    cloud_folder=settings.cloudinary_folder,
)


def upload_image(file: BinaryIO) -> str:
    """
    The upload_image function takes a file, uploads it to Cloudinary, and returns the URL of the uploaded image.

    :param file: BinaryIO: Pass in the file to be uploaded
    :param return_size: tuple[int, int]: Set the width and height of the image
    :param auth: Auth: Authentication service instance
    :return: The URL of the uploaded image
    :doc-author: kagev
    """
    file_id = settings.cloudinary_folder + "/" + f"avatar_{uuid.uuid4()}"
    upload(file, public_id=file_id, tag="web_project", overwrite=True)
    img_url = cloudinary.CloudinaryImage(file_id).build_url(
        # width=return_size[0],
        # height=return_size[1],
        # crop="fill",
        version=resource(file_id)["version"],
    )
    return {"image id": file_id, "URL": img_url}


def transform_img(public_id, width, height, crop):
    """
    The transform_img function takes a Cloudinary public_id and an optional quality parameter to optimize the image.

    :param public_id: Public ID of the image to optimize
    :type public_id: str
    :param width: set the image width for cropping
    :type width: int
    :param height: set the image height for cropping
    :type height: int
    :param crop: Cropping modes: If the requested dimensions have a different aspect ratio than the original, these modes crop out part of the image.
    fill, lfill, fill_pad, crop,thumb
    :type crop: str
    :return: The returns us images from Cloudinary transformed_url
    :doc-author: kagev
    """

    transformed_url = cloudinary.uploader.explicit(
        public_id,
        type="upload",
        eager=[
            {"gravity": "auto", "height": height, "width": width, "crop": crop},
            {"fetch_format": "auto"},
            {"radius": "max"},
        ],
    )

    return transformed_url["secure_url"]


def optimize_media(public_id, quality=80):
    """
    The optimize_media function takes a Cloudinary public_id and an optional quality parameter to optimize the image.

    :param public_id: str: Public ID of the image to optimize
    :param quality: int: Image quality (0-100), where 0 is the lowest quality and 100 is the highest.
    :return: The response from Cloudinary
    :doc-author: kagev
    """
    # Set quality for optimization

    optimize_img = cloudinary.uploader.explicit(
        public_id,
        type="upload",
        eager=[
            {"quality": quality},
        ],
    )
    return optimize_img["secure_url"]
