import asyncio
import subprocess
from io import BytesIO
from pathlib import Path

from PIL import Image

from puppy_vacation_diary.core.config import settings

THUMB_SIZE = (settings.thumbnail_size, settings.thumbnail_size)
THUMB_FORMAT = "WEBP"
THUMB_QUALITY = 85


def _resize_image(image_bytes: bytes) -> bytes:
    img = Image.open(BytesIO(image_bytes))
    img.thumbnail(THUMB_SIZE)
    buf = BytesIO()
    img.save(buf, format=THUMB_FORMAT, quality=THUMB_QUALITY)
    return buf.getvalue()


def _extract_video_frame(video_path: str, output_path: str) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vframes", "1",
            "-vf", f"scale={THUMB_SIZE[0]}:{THUMB_SIZE[1]}:force_original_aspect_ratio=2,crop={THUMB_SIZE[0]}:{THUMB_SIZE[1]}",
            output_path,
        ],
        capture_output=True,
        check=True,
    )


async def make_photo_thumbnail(image_bytes: bytes) -> bytes:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _resize_image, image_bytes)


async def make_video_thumbnail(video_path: str, thumb_path: str) -> None:
    loop = asyncio.get_running_loop()
    # ffmpeg may lack WEBP encoder, so extract as PNG then convert with Pillow
    tmp_png = str(Path(thumb_path).with_suffix(".png"))
    await loop.run_in_executor(None, _extract_video_frame, video_path, tmp_png)
    png_bytes = await loop.run_in_executor(None, _read_file_bytes, tmp_png)
    webp_bytes = await loop.run_in_executor(None, _resize_image, png_bytes)
    await loop.run_in_executor(None, _write_file_bytes, thumb_path, webp_bytes)
    await loop.run_in_executor(None, _remove_file, tmp_png)


def _read_file_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


def _write_file_bytes(path: str, data: bytes) -> None:
    Path(path).write_bytes(data)


def _remove_file(path: str) -> None:
    Path(path).unlink(missing_ok=True)
