from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.models import User
from src.database.connection import get_db
from src.repository import image as repository_image
from src.services.auth import auth_service
from ..schemas.image import ImageModel


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/uploadimage/", response_model=ImageModel)
async def create_image(
    file: UploadFile = File(),
    description: str = Form(),
    tags: List[str] = Form([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> ImageModel:
    """
    Endpoint for uploading an image by the user.
    Parameters:
        :param file: str: image file uploaded by the user.
        :param description: str: describing the image.
        :param tags: a list of strings representing tags associated with the image.
        :param db: SQLAlchemy database session object.
        :param current_user: a user object representing the currently authenticated user.
        :return: ImageModel: модель изображения с полями id, user_id, description и tags.
    """

    # Попытка создать изображение
    image = await repository_image.create_image(
        file, current_user.id, description, tags, db
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
) -> ImageModel:
    """
    Endpoint for retrieving an image by its ID.
    Parameters:
        :param image_id: str: image ID.
        :param current_user: a user object representing the currently authenticated user.
        :param db: SQLAlchemy database session object.
        :return: image model with path, user id, description and tags fields.
    Raises:
        HTTPException: 403 Forbidden, if the user is not an administrator or the owner of the image.
        HTTPException: 404 Not Found, if the image is not found.
    """


    image = await repository_image.get_image(image_id, db, user_id=current_user.id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    elif not (
        current_user.role in ("admin", "moderator") or current_user.id == image.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
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
) -> dict:
    """
    Endpoint for updating the image description.
    Parameters:
        :param image_id: image id
        :param description: new image description.
        :param current_user: a user object representing the currently authenticated user.
        :param db: SQLAlchemy database session object.
        :return: dict: dictionary with a message about successful update.
    Raises:
        HTTPException: 403 Forbidden, if the user is not an administrator or the owner of the image.
        HTTPException: 404 Not Found, if the image is not found.
    """

    image = await repository_image.get_image(image_id, db, user_id=current_user.id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    elif not (
        current_user.role in ("admin", "moderator") or current_user.id == image.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    description = await repository_image.change_description(image_id, description, db)

    return {"message": "Image update successesful"}


@router.delete("/deleteimage/{image_id}", response_model=ImageModel)
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> dict:
    """
    Endpoint for deleting an image by its ID.
    Parameters:
        :param image_id:  image id
        :param db:
        :param current_user: a user object representing the currently authenticated user.
        :return:
    Returns:
        :return: dict: dictionary with a message about successful deletion.

    Raises:
    HTTPException: 403 Forbidden, if the user is not an administrator or the owner of the image.
    HTTPException: 404 Not Found, if the image is not found.
    """

    image = await repository_image.get_image(image_id, current_user.id, db)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    elif not (
        current_user.role in ("admin", "moderator") or current_user.id == image.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    image = await repository_image.delte_image_by_id(image_id, db)

    return {"message": "Image deleted successfully"}
