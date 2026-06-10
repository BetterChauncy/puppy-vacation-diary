import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from puppy_vacation_diary.core.config import settings
from puppy_vacation_diary.models.base import Base


async def migrate():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate())
