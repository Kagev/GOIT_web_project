from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database.models import Photo, Tag
from typing import List
import shutil
from sqlalchemy import and_


def create_image(
    file, user_id: int, description: str, tags: List[str], db: Session
) -> Photo:
    """
    Создает изображение, сохраняет его на сервере и связывает его с тегами.

    Parameters:
    - file: загружаемый файл изображения.
    - user_id: идентификатор пользователя, загружающего изображение.
    - description: описание изображения.
    - tags: список тегов, связанных с изображением.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - Photo: объект Photo, представляющий созданное изображение.
    """
    # Создание объекта Photo
    image = Photo(user_id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)

    # Перебор тегов и создание или получение из базы данных
    for tag_name in tags:
        try:
            # Попытка найти тег в базе данных
            tag = db.query(Tag).filter(Tag.name == tag_name).one()
        except NoResultFound:
            # Создание нового тега, если не найден
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()

        # Присоединение тега к изображению
        image.tags.append(tag)

    # Сохранение файла изображения на сервере
    with open(f"images/{image.id}_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Обновление пути к файлу изображения в объекте Photo
    image.path = f"images/{image.id}_{file.filename}"
    db.commit()

    # Возвращение объекта Photo
    return image


async def get_image(image_id: int, user_id: int, db: Session):
    """
    Получает изображение по его идентификатору и идентификатору пользователя.

    Parameters:
    - image_id: идентификатор изображения.
    - user_id: идентификатор пользователя.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - Photo: объект Photo, представляющий запрашиваемое изображение, или None, если изображение не найдено.
    """
    return (
        db.query(Photo)
        .filter(and_(Photo.id == image_id, Photo.user_id == user_id))
        .first()
    )


async def change_description(
    image_id: int, user_id: int, description: str, db: Session
):
    """
    Изменяет описание изображения.

    Parameters:
    - image_id: идентификатор изображения.
    - user_id: идентификатор пользователя.
    - description: новое описание изображения.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - Optional[Photo]: объект Photo, представляющий измененное изображение, или None, если изображение не найдено.
    """
    # Поиск изображения по идентификаторам
    image = (
        db.query(Photo)
        .filter(and_(Photo.id == image_id, Photo.user_id == user_id))
        .first()
    )

    # Если изображение найдено, изменение описания и сохранение изменений в базе данных
    if image:
        image.description = description
        db.commit()

    return image


async def delte_image_by_id(image_id: int, user_id: int, db: Session) -> bool:
    """
    Удаляет изображение по его идентификатору и идентификатору пользователя.

    Parameters:
    - image_id: идентификатор изображения.
    - user_id: идентификатор пользователя.
    - db: объект сессии базы данных SQLAlchemy.

    Returns:
    - bool: True, если изображение успешно удалено, иначе False.
    """
    # Поиск и удаление изображения из базы данных
    image = (
        db.query(Photo)
        .filter(and_(Photo.id == image_id, Photo.user_id == user_id))
        .delete()
    )

    # Сохранение изменений в базе данных
    if image:
        db.commit()

    return image
