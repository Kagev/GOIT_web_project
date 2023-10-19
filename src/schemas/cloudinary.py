from pydantic import BaseModel
from typing import List, Optional


class CloudinaryResource(BaseModel):
    public_id: str
    format: Optional[str]
    version: Optional[int]
    resource_type: Optional[str]
    created_at: Optional[str]
    tags: Optional[List[str]]
    bytes: Optional[int]
    width: Optional[int]
    height: Optional[int]
    url: Optional[str]
    secure_url: Optional[str]
    next_cursor: Optional[str]
    transformation: Optional[str]
    pages: Optional[str]
