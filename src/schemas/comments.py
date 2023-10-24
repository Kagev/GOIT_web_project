from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime

from .users import UserDb
from .image import ImageModel


class CommentModel(BaseModel):
    content: str = Field(min_length=1, max_length=255)


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: int
    user: UserDb
    image: ImageModel
    created_at: datetime
    updated_at: datetime