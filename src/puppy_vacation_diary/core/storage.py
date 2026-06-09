import os
from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import UploadFile

from puppy_vacation_diary.core.config import settings


class StorageBackend(ABC):
    @abstractmethod
    async def save(self, file: UploadFile, key: str) -> str:
        ...

    @abstractmethod
    async def save_bytes(self, data: bytes, key: str) -> str:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...

    @abstractmethod
    def get_url(self, key: str) -> str:
        ...


class LocalStorage(StorageBackend):
    def __init__(self) -> None:
        self.base_dir = Path(settings.upload_dir)

    async def save(self, file: UploadFile, key: str) -> str:
        dest = self.base_dir / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = await file.read()
        dest.write_bytes(content)
        return key

    async def save_bytes(self, data: bytes, key: str) -> str:
        dest = self.base_dir / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return key

    async def delete(self, key: str) -> None:
        path = self.base_dir / key
        if path.exists():
            path.unlink()

    def get_url(self, key: str) -> str:
        return f"/uploads/{key}"


def get_storage() -> StorageBackend:
    if settings.storage_backend == "s3":
        msg = "S3 storage not yet implemented"
        raise NotImplementedError(msg)
    return LocalStorage()
