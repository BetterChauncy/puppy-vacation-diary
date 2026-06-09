import datetime

from pydantic import BaseModel


class MediaResponse(BaseModel):
    model_config = {"from_attributes": True}

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


class PaginatedMediaResponse(BaseModel):
    items: list[MediaResponse]
    total: int
    limit: int
    offset: int


class CommentCreate(BaseModel):
    content: str


class CommentUser(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    nickname: str | None = None
    avatar: str | None = None


class CommentResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    media_id: int
    user: CommentUser | None = None
    content: str
    created_at: datetime.datetime
