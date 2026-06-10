import asyncio
import logging
import os
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy import func as sa_func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from puppy_vacation_diary.core.config import settings
from puppy_vacation_diary.core.dependencies import get_current_user, get_db
from puppy_vacation_diary.core.storage import get_storage
from puppy_vacation_diary.core.thumbnails import make_photo_thumbnail, make_video_thumbnail
from puppy_vacation_diary.models.comment import Comment
from puppy_vacation_diary.models.media import Media
from puppy_vacation_diary.models.pet import Pet
from puppy_vacation_diary.models.user import User
from puppy_vacation_diary.schemas.media import (
    CommentCreate,
    CommentResponse,
    CommentUser,
    MediaResponse,
    PaginatedMediaResponse,
)

router = APIRouter(tags=["media"])

IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
VIDEO_TYPES = {"video/mp4", "video/quicktime", "video/x-msvideo"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".heif"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".webm", ".mkv"}


def _ext(file_name: str) -> str:
    return Path(file_name).suffix or ""


def _media_type(mime: str, filename: str = "") -> str:
    if mime in IMAGE_TYPES:
        return "photo"
    if mime in VIDEO_TYPES:
        return "video"
    ext = Path(filename).suffix.lower()
    if ext in IMAGE_EXTS:
        return "photo"
    if ext in VIDEO_EXTS:
        return "video"
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported file type: {mime}")


def _thumb_subdir(mtype: str) -> str:
    return f"{mtype}s/thumbs"


def _file_subdir(mtype: str) -> str:
    return f"{mtype}s"


@router.post("/pets/{pet_id}/media", response_model=list[MediaResponse], status_code=status.HTTP_201_CREATED)
async def upload_media(
    pet_id: int,
    files: list[UploadFile],
    db: AsyncSession = Depends(get_db),
) -> list[Media]:
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    storage = get_storage()
    results: list[Media] = []

    for file in files:
        mime = file.content_type or "application/octet-stream"
        mtype = _media_type(mime, file.filename or "")
        ext = _ext(file.filename or "file")
        uid = str(uuid.uuid4())
        file_key = f"{pet_id}/{_file_subdir(mtype)}/{uid}{ext}"
        thumb_key = f"{pet_id}/{_thumb_subdir(mtype)}/{uid}.webp"

        raw = await file.read()
        file_size = len(raw)

        await storage.save_bytes(raw, file_key)

        if mtype == "photo":
            thumb_bytes = await make_photo_thumbnail(raw)
            await storage.save_bytes(thumb_bytes, thumb_key)
        else:
            upload_dir = settings.upload_dir
            local_path = str(Path(upload_dir) / file_key)
            thumb_local = str(Path(upload_dir) / thumb_key)
            Path(thumb_local).parent.mkdir(parents=True, exist_ok=True)

            # Transcode HEVC/H.265 → H.264 for broad mini program compatibility
            new_file_key = file_key.rsplit(".", 1)[0] + ".mp4"
            new_local_path = str(Path(upload_dir) / new_file_key)
            tmp_path = local_path + "_h264.mp4"

            async def _transcode(audio_opt: str) -> tuple[int, bytes]:
                args = [
                    "ffmpeg", "-y",
                    "-i", local_path,
                    "-c:v", "libx264",
                    "-profile:v", "baseline",
                    "-pix_fmt", "yuv420p",
                    "-preset", "medium",
                    "-crf", "23",
                    "-movflags", "+faststart",
                ]
                if audio_opt:
                    args.extend(["-c:a", audio_opt])
                else:
                    args.append("-an")
                args.append(tmp_path)
                proc = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                _, stderr = await proc.communicate()
                return proc.returncode, stderr

            ret, stderr = await _transcode("aac")
            if ret != 0:
                logger.warning(
                    "ffmpeg aac failed (ret=%d), retrying without audio. stderr=%s",
                    ret, stderr.decode(errors="replace")[-500:],
                )
                ret, stderr = await _transcode("")

            if ret == 0:
                with open(tmp_path, "rb") as f:
                    transcoded = f.read()
                await storage.save_bytes(transcoded, new_file_key)
                if new_file_key != file_key:
                    await storage.delete(file_key)
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
                file_key = new_file_key
                local_path = new_local_path
                file_size = len(transcoded)
            else:
                logger.error(
                    "ffmpeg all attempts failed for %s, keeping original. stderr=%s",
                    file_key, stderr.decode(errors="replace")[-500:],
                )

            await make_video_thumbnail(local_path, thumb_local)

        media = Media(
            pet_id=pet_id,
            media_type=mtype,
            file_key=file_key,
            thumbnail_key=thumb_key,
            original_filename=file.filename or "unknown",
            file_size=file_size,
            mime_type=mime,
        )
        db.add(media)
        await db.flush()
        await db.refresh(media)
        results.append(media)

    return results


@router.get("/pets/{pet_id}/media", response_model=PaginatedMediaResponse)
async def list_media(
    pet_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> PaginatedMediaResponse:
    total_q = select(sa_func.count()).select_from(Media).where(Media.pet_id == pet_id)
    total = (await db.execute(total_q)).scalar() or 0
    result = await db.execute(
        select(Media)
        .where(Media.pet_id == pet_id)
        .order_by(Media.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    items = list(result.scalars().all())
    return PaginatedMediaResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/media/{media_id}", response_model=MediaResponse)
async def get_media(media_id: int, db: AsyncSession = Depends(get_db)) -> Media:
    media = await db.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    return media


@router.delete("/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(media_id: int, db: AsyncSession = Depends(get_db)) -> None:
    media = await db.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    storage = get_storage()
    await storage.delete(media.file_key)
    if media.thumbnail_key:
        await storage.delete(media.thumbnail_key)

    await db.delete(media)
    await db.flush()


@router.post("/media/{media_id}/like")
async def toggle_like(media_id: int, liked: bool = True, db: AsyncSession = Depends(get_db)):
    media = await db.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    if liked:
        media.likes_count = Media.likes_count + 1
    else:
        media.likes_count = Media.likes_count - 1
    await db.flush()
    await db.refresh(media)
    return {"likes_count": media.likes_count}


@router.post("/media/{media_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    media_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_current_user),
) -> Comment:
    media = await db.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    comment = Comment(media_id=media_id, user_id=user.id if user else None, content=data.content)
    db.add(comment)
    await db.flush()
    await db.refresh(comment)
    return comment


@router.get("/media/{media_id}/comments", response_model=list[CommentResponse])
async def list_comments(media_id: int, db: AsyncSession = Depends(get_db)) -> list[Comment]:
    result = await db.execute(
        select(Comment)
        .options(joinedload(Comment.user))
        .where(Comment.media_id == media_id)
        .order_by(Comment.created_at.desc())
    )
    return list(result.unique().scalars().all())


@router.delete("/media/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)) -> None:
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    await db.delete(comment)
    await db.flush()
