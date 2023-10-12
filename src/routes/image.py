from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List
from src.database.models import Image, Tag
from src.schemas import ImageModel
from src.database.db import get_db
import shutil

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/uploadimage/", response_model=ImageModel)
async def create_image(
    file: UploadFile = File(),
    description: str = Form,
    tags: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    image = Image(description=description)
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

    return {"id": image.id, "description": description, "tags": [tag.name for tag in image.tags]}



@router.delete('/deleteimage/{image_id}', response_model=ImageModel):
async def delete_image(image_id:int, db:Session(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    db.query(Image).filter(Image.id == image_id).delete()
    db.commit()

    return {"message": "Image deleted successfully"}


@router.put('/updateimage/{iamge_id}', response_model=ImageModel)
async def update_image(image_id:int, description:str = Form(), db:Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    image.description = description
    db.commit()

    return {'message':'Image update successesful'}


@router.get('/getimage/{image_id}', response_model=ImageModel)
async def get_image(image_id:int, db:Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    
    return {"path": image.path, "description": image.description, "tags": [tag.name for tag in image.tags]}