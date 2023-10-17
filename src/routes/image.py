from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session
from typing import List
from src.services.auth import TokenData
from schemas import ImageModel
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
    token_data: TokenData = Depends(auth_service.get_token_data),
) -> ImageModel:
    """
    Эндпоинт для загрузки изображения пользователем.

    Parameters:
    - file: файл изображения, загружаемый пользователем.
    - description: строка, описывающая изображение.
    - tags: список строк, представляющих теги, связанные с изображением.
    - db: объект сессии базы данных SQLAlchemy.
    - token_data: объект данных токена, представляющий текущего аутентифицированного пользователя.

    Returns:
    - ImageModel: модель изображения с полями id, user_id, description и tags.

    """
    # Попытка создать изображение
    image = await repository_image.create_image(
        file, description, tags, db, user_id=token_data.user_id
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
    token_data: TokenData = Depends(auth_service.get_token_data),
    db: Session = Depends(get_db),
) -> ImageModel:
    """
    Эндпоинт для получения изображения по его идентификатору.

    Parameters:
    - image_id: идентификатор изображения.
    - token_data: объект данных токена, представляющий текущего аутентифицированного пользователя.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - ImageModel: модель изображения с полями path, user_id, description и tags.

    Raises:
    - HTTPException: 403 Forbidden, если пользователь не администратор и не владелец изображения.
    - HTTPException: 404 Not Found, если изображение не найдено.
    """
    image = await repository_image.get_image(image_id, db, user_id=token_data.user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    elif not (token_data.role in ("admin", 'moderator') or token_data.user_id == image.user_id):
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
    token_data: TokenData = Depends(auth_service.get_token_data),
    db: Session = Depends(get_db),
) -> dict:
    """
    Эндпоинт для обновления описания изображения.

    Parameters:
    - image_id: идентификатор изображения.
    - description: новое описание изображения.
    - token_data: объект данных токена, представляющий текущего аутентифицированного пользователя.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - dict: словарь с сообщением об успешном обновлении.

    Raises:
    - HTTPException: 403 Forbidden, если пользователь не администратор и не владелец изображения.
    - HTTPException: 404 Not Found, если изображение не найдено.
    """
    image = await repository_image.get_image(image_id, db, user_id=token_data.user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    elif not (token_data.role in ("admin", 'moderator') or token_data.user_id == image.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    description = await repository_image.change_description(image_id, description, db)

    return {"message": "Image update successesful"}


@router.delete("/deleteimage/{image_id}", response_model=ImageModel)
async def delete_image(
    image_id: int,
    db: Session(get_db),
    token_data: TokenData = Depends(auth_service.get_token_data),
) -> dict:
    """
    Эндпоинт для удаления изображения по его идентификатору.

    Parameters:
    - image_id: идентификатор изображения.
    - db: объект сессии базы данных SQLAlchemy.
    - token_data: объект данных токена, представляющий текущего аутентифицированного пользователя.

    Returns:
    - dict: словарь с сообщением об успешном удалении.

    Raises:
    - HTTPException: 403 Forbidden, если пользователь не администратор и не владелец изображения.
    - HTTPException: 404 Not Found, если изображение не найдено.
    """
    image = await repository_image.get_image(image_id, db, user_id=token_data.user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    elif not (token_data.role in ("admin", 'moderator') or token_data.user_id == image.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    image = await repository_image.delte_image_by_id(image_id, db)

    return {"message": "Image deleted successfully"}
