from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
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
    description: str = Form(),
    tags: List[str] = Form([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user_as_admin),
) -> ImageModel:
    """
    Эндпоинт для загрузки изображения пользователем.

    Parameters:
    - file: файл изображения, загружаемый пользователем.
    - description: строка, описывающая изображение.
    - tags: список строк, представляющих теги, связанные с изображением.
    - db: объект сессии базы данных SQLAlchemy.
    - current_user: объект пользователя, представляющий текущего аутентифицированного пользователя.

    Returns:
    - ImageModel: модель изображения с полями id, user_id, description и tags.

    """
    # Попытка создать изображение
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
    current_user: User = Depends(auth_service.get_current_user_as_admin),
    db: Session = Depends(get_db),
) -> ImageModel:
    """
    Эндпоинт для получения изображения по его идентификатору.

    Parameters:
    - image_id: идентификатор изображения.
    - current_user: объект пользователя, представляющий текущего аутентифицированного пользователя.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - ImageModel: модель изображения с полями path, user_id, description и tags.

    Raises:
    - HTTPException: 404 Not Found, если изображение не найдено.
    """
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
    current_user: User = Depends(auth_service.get_current_user_as_admin),
    db: Session = Depends(get_db),
) -> dict:
    """
    Эндпоинт для обновления описания изображения.

    Parameters:
    - image_id: идентификатор изображения.
    - description: новое описание изображения.
    - current_user: объект пользователя, представляющий текущего аутентифицированного пользователя.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - dict: словарь с сообщением об успешном обновлении.

    Raises:
    - HTTPException: 404 Not Found, если изображение не найдено.
    """
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
    current_user: User = Depends(auth_service.get_current_user_as_admin),
) -> dict:
    """
    Эндпоинт для удаления изображения по его идентификатору.

    Parameters:
    - image_id: идентификатор изображения.
    - db: объект сессии базы данных SQLAlchemy.
    - current_user: объект пользователя, представляющий текущего аутентифицированного пользователя.

    Returns:
    - dict: словарь с сообщением об успешном удалении.

    Raises:
    - HTTPException: 404 Not Found, если изображение не найдено.
    """
    image = await repository_image.get_image(image_id, db, user_id=current_user.id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    image = await repository_image.delte_image_by_id(image_id, db)

    return {"message": "Image deleted successfully"}
