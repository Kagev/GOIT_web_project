from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.models import Photo, Tag, User
from src.schemas import ImageModel
from src.database.db import get_db
from src.repository import image as repository_image
from src.services.auth import auth_service

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/uploadimage/", response_model=ImageModel)
async def create_image(
    file: UploadFile = File(),
    description: str = Form,
    tags: List[str] = Form([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    image = await repository_image.create_image(
        file, description, tags, db, user_id=current_user.id
    )

    return {
        "id": image.id,
        "user_id": image.user_id,
        "description": description,
        "tags": [tag.name for tag in image.tags],
    }


@router.get("/getimage/{image_id}", response_model=ImageModel)
async def get_image(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    image = await repository_image.get_image(image_id, db, user_id=current_user.id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    return {
        "path": image.path,
        "user_id": image.user_id,
        "description": image.description,
        "tags": [tag.name for tag in image.tags],
    }


@router.put("/updateimage/{iamge_id}", response_model=ImageModel)
async def update_image(
    image_id: int,
    description: str = Form(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    image = await repository_image.get_image(image_id, db, user_id=current_user.id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    description = await repository_image.change_description(image_id, description, db)

    return {"message": "Image update successesful"}


@router.delete("/deleteimage/{image_id}", response_model=ImageModel)
async def delete_image(
    image_id: int,
    db: Session(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    image = await repository_image.get_image(image_id, db, user_id=current_user.id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    image = await repository_image.delte_image_by_id(image_id, db)

    return {"message": "Image deleted successfully"}
