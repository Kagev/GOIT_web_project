from pydantic import BaseModel, Field


class ImageModel(BaseModel):
    id: int
    path: str
    description: str
    tags: str = Field(min_length=0, max_length=5)

    class Config:
        orm_mode = True


class TagModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
