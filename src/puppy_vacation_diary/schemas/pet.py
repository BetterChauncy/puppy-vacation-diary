import datetime

from pydantic import BaseModel


class PetCreate(BaseModel):
    name: str
    species: str
    gender: str
    age: int
    avatar: str | None = None
    address: str | None = None
    birthday: datetime.date | None = None
    bio: str | None = None
    is_homepage: bool = False


class PetUpdate(BaseModel):
    name: str | None = None
    species: str | None = None
    gender: str | None = None
    age: int | None = None
    avatar: str | None = None
    address: str | None = None
    birthday: datetime.date | None = None
    bio: str | None = None
    is_homepage: bool | None = None


class PetResponse(BaseModel):
    id: int
    name: str
    species: str
    gender: str
    age: int
    avatar: str | None = None
    address: str | None = None
    birthday: datetime.date | None = None
    bio: str | None = None
    is_homepage: bool = False
