from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database.models import Image, Tag
from typing import List
import shutil
from sqlalchemy import and_


async def create_image(
    file, user_id: int, description: str, tags: List[str], db: Session
) -> Image:
    """
    Creates an image, stores it on the server, and associates it with tags.

    Parameters:
    - file: image file to load.
    - user_id: ID of the user uploading the image.
    - description: description of the image.
    - tags: list of tags associated with the image.
    - db: SQLAlchemy database session object.

    Returns:
    - Images: An Images object representing the generated image.
    """
    # Creating an Image Object
    image = Image(user_id=user_id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)

    # Iterate over tags and create or get from database
    for tag_name in tags:
        try:
            # Trying to find a tag in the database
            tag = db.query(Tag).filter(Tag.name == tag_name).one()
        except NoResultFound:
            # Create a new tag if not found
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()

        # Attaching a tag to an image
        image.tags.append(tag)

    # Saving an image file on the server
    with open(f"images/{image.id}_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Updating the path to an image file in an Image object
    image.path = f"images/{image.id}_{file.filename}"
    db.commit()

    # Returning an Image object
    return image


async def get_image(image_id: int, user_id: int, db: Session):
    """
        Retrieves an image by its ID and user ID.

        Parameters:
        - image_id: image identifier.
        - user_id: user identifier.
        - db: SQLAlchemy database session object.

        Returns:
        - Image: An Image object representing the requested image, or None if no image was found.
        """
    return (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == user_id))
        .first()
    )


async def change_description(
    image_id: int, user_id: int, description: str, db: Session
):
    """
    Changes the image description.

    Parameters:
    - image_id: image identifier.
    - user_id: user identifier.
    - description: new description of the image.
    - db: SQLAlchemy database session object.

    Returns:
    - Optional[Image]: An Image object representing the modified image, or None if no image was found.
    """
    # Search for an image by identifiers
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == user_id))
        .first()
    )

    # If an image is found, change the description and save the changes to the database
    if image:
        image.description = description
        db.commit()

    return image


async def delte_image_by_id(image_id: int, user_id: int, db: Session) -> bool:
    """
    Deletes an image by its ID and user ID.

    Parameters:
    - image_id: image identifier.
    - user_id: user identifier.
    - db: SQLAlchemy database session object.

    Returns:
    - bool: True if the image was successfully deleted, otherwise False.
    """
    # Search and remove an image from the database
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == user_id))
        .delete()
    )

    # Saving changes to the database
    if image:
        db.commit()

    return image
