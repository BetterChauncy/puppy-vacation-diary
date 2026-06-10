"""
One-time migration: transcode existing HEVC videos to H.264.
Usage: uv run python -m puppy_vacation_diary.migrate_videos
"""
import asyncio
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from puppy_vacation_diary.core.config import settings
from puppy_vacation_diary.models.media import Media


async def main():
    database_url = settings.database_url
    if database_url.startswith("sqlite"):
        database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")
    engine = create_async_engine(database_url)

    async with AsyncSession(engine) as db:
        result = await db.execute(select(Media).where(Media.media_type == "video"))
        videos = result.scalars().all()

    if not videos:
        print("No existing videos found.")
        return

    upload_dir = Path(settings.upload_dir)
    converted = 0

    for v in videos:
        src = upload_dir / v.file_key
        if not src.exists():
            print(f"  SKIP  {v.file_key} — file not found")
            continue

        codec = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=codec_name", "-of", "csv=p=0",
             str(src)],
            capture_output=True, text=True,
        ).stdout.strip()

        if codec == "h264":
            print(f"  SKIP  {v.file_key} — already H.264 ({codec})")
            continue

        if v.file_key.endswith(".mp4"):
            new_key = v.file_key
            dst = src
        else:
            new_key = v.file_key.rsplit(".", 1)[0] + ".mp4"
            dst = upload_dir / new_key

        tmp = src.with_name(src.name + "_h264_tmp.mp4")
        print(f"  TRANSCODE  {v.file_key} (codec={codec}) → {new_key}")
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(src),
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac", "-movflags", "+faststart",
                str(tmp),
            ],
            capture_output=True,
            check=True,
        )

        if dst != src:
            tmp.replace(dst)
            src.unlink(missing_ok=True)
        else:
            tmp.replace(src)

        v.file_key = new_key
        v.file_size = dst.stat().st_size
        converted += 1

    async with AsyncSession(engine) as db:
        for v in videos:
            db.add(v)
        await db.commit()

    print(f"\nDone. {converted} video(s) transcoded.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
