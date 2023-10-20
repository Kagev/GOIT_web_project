from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from ..services.cloudinary import upload_image, transform_img, optimize_media

router = APIRouter(prefix="/cloudinary", tags=["cloudinary"])


# uploading an image to Cloudinary
@router.post("/upload/")
async def upload_image_route(file: UploadFile = File(...), user_id: int = 0) -> object:
	"""
	Service for Upload image
	:return:
	:param file: str
	:param user_id: int
	:return: Response
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
	Service for transformation image
	:param public_id: int
	:param width: int
	:param height: int
	:param crop: str
	:return: Transform image
	:doc-author: kagev
	"""
	transformed_url = transform_img(public_id, width, height, crop)
	return {"transformed_url": transformed_url}


# Media optimization
@router.post("/optimize/")
async def optimize_image(public_id: str, quality: int = 80) -> object:
	"""
	Service for optimization image
	:param public_id: str
	:param quality: int
	:return: Result optimization image
	:doc-author: kagev
	"""
	result = optimize_media(public_id, quality)
	return {"result": result}
