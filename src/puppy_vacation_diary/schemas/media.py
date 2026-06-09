import datetime

from pydantic import BaseModel


class MediaResponse(BaseModel):
    id: int
    pet_id: int
    media_type: str
    file_key: str
    thumbnail_key: str | None = None
    original_filename: str
    file_size: int
    mime_type: str
    likes_count: int = 0
    created_at: datetime.datetime


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    media_id: int
    content: str
    created_at: datetime.datetime
