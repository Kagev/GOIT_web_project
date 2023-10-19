from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File

from ..services.cloudinary import upload_image, transform_img, optimize_media


router = APIRouter(prefix="/cloudinary", tags=["cloudinary"])



# Announcing the route for uploading an image to Cloudinary
# Завантаження зображень на сервер
@router.post("/upload/")
async def upload_image_route(file: UploadFile = File(...), user_id: int = 0):
	if file.content_type.startswith("image"):
		image_url = upload_image(file.file, user_id)
		return {"image_url": image_url}
	return JSONResponse(status_code=415, content="Unsupported Media Type")


# Трансформація зображень
@router.post("/transform/")
async def transform_image(public_id: str, width: int, height: int, crop: str):
	transformed_url = transform_img(public_id, width, height, crop)
	return {"transformed_url": transformed_url}


# Оптимізація медіа
@router.post("/optimize/")
async def optimize_image(public_id: str, quality: int = 80):
	result = optimize_media(public_id, quality)
	return {"result": result}
