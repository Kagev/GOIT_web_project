from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from src.services.cloudinary import upload_image, transform_img, optimize_media

router = APIRouter(prefix="/cloudinary", tags=["cloudinary"])


# uploading an image to Cloudinary
@router.post("/upload/")
async def upload_image_route(file: UploadFile = File(...), user_id: int = 0) -> object:
	"""
	The upload_image function takes a file, uploads it to Cloudinary, and returns the URL of the uploaded image.

	    :param file: BinaryIO: Pass in the file to be uploaded
	    :param return_size: tuple[int, int]: Set the width and height of the image
	    :param auth: Auth: Authentication service instance
	    :return: The URL of the uploaded image
	    :doc-author: kagev
	"""

	if file.content_type.startswith("image"):
		image_url = upload_image(file.file, user_id)
		return {"image_url": image_url}
	return JSONResponse(status_code=415, content="Unsupported Media Type")


# Image transformation
@router.post("/transform/")
async def transform_image(public_id: str, width: int, height: int, crop: str) -> object:
	"""
    The transform_img function takes a Cloudinary public_id and an optional quality parameter to optimize the image.

	    :param public_id: Public ID of the image to optimize
	    :type public_id: str
	    :param width: set the image width for cropping
	    :type width: int
	    :param height: set the image height for cropping
	    :type height: int
	    :param crop: Cropping modes: If the requested dimensions have a different aspect ratio than the original, these modes crop out part of the image. EXAMPLE: fill, lfill, fill_pad, crop,thumb
	    :type crop: str
	    :return: The returns us images from Cloudinary transformed_url
	    :doc-author: kagev
    """

	transformed_url = transform_img(public_id, width, height, crop)

	return {"transformed_url": transformed_url}


# Media optimization
@router.post("/optimize/")
async def optimize_image(public_id: str, quality: int = 80) -> object:
	"""
    Service for optimizing an image.

	    :param public_id: The public ID of the image to optimize.
	    :type public_id: str
	    :param quality: The desired quality of the optimized image.
	    :type quality: int
	    :return: The result of the optimization.
	    :rtype: dict
    """

	result = optimize_media(public_id, quality)
	return {"result": result}
