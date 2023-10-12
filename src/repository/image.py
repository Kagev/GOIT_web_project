from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database.models import Photo, Tag
from typing import List
import shutil
from sqlalchemy import and_


async def create_image(file, user_id: int, description: str, tags: List, db: Session):
    image = Photo(user_id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)

    for tag_name in tags:
        try:
            tag = db.query(Tag).filter(Tag.name == tag_name).one()
        except NoResultFound:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()

        image.tags.append(tag)

    with open(f"images/{image.id}_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image.path = f"images/{image.id}_{file.filename}"
    db.commit()

    return image


async def get_image(image_id: int, user_id: int, db: Session):
    return (
        db.query(Photo)
        .filter(and_(Photo.id == image_id, Photo.user_id == user_id))
        .first()
    )


async def change_description(
    image_id: int, user_id: int, description: str, db: Session
):
    image = (
        db.query(Photo)
        .filter(and_(Photo.id == image_id, Photo.user_id == user_id))
        .first()
    )
    if image:
        image.description = description
        db.commit()

    return image


async def delte_image_by_id(image_id: int, user_id: int, db: Session):
    image = (
        db.query(Photo)
        .filter(and_(Photo.id == image_id, Photo.user_id == user_id))
        .delete()
    )
    if image:
        db.commit()

    return image
