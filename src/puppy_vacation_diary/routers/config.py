import random
from datetime import date, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from puppy_vacation_diary.core.config import settings
from puppy_vacation_diary.core.dependencies import get_db
from puppy_vacation_diary.models.pet import Pet
from puppy_vacation_diary.models.site_config import SiteConfig
from puppy_vacation_diary.schemas.config import ConfigUpdate

router = APIRouter(tags=["config"])


def _pick_homepage_pet(pets: list[Pet], rotation: str) -> int | None:
    if not pets:
        return None
    if len(pets) == 1:
        return pets[0].id
    if rotation == "hourly":
        seed = str(datetime.utcnow().hour)
    else:
        seed = str(date.today())
    return random.Random(seed).choice(pets).id


async def _get_or_create_config(db: AsyncSession) -> SiteConfig:
    config = await db.get(SiteConfig, 1)
    if config is None:
        config = SiteConfig(id=1)
        db.add(config)
        await db.flush()
    return config


@router.get("/config")
async def get_config(db: AsyncSession = Depends(get_db)):
    site_config = await _get_or_create_config(db)
    result = await db.execute(select(Pet).where(Pet.is_homepage == True))
    homepage_pets = list(result.scalars().all())
    return {
        "app_name": settings.app_name,
        "homepage_pet_id": _pick_homepage_pet(homepage_pets, site_config.homepage_rotation),
        "homepage_pet_ids": [p.id for p in homepage_pets],
        "homepage_rotation": site_config.homepage_rotation,
    }


@router.put("/config")
async def update_config(data: ConfigUpdate, db: AsyncSession = Depends(get_db)):
    site_config = await _get_or_create_config(db)
    site_config.homepage_rotation = data.homepage_rotation
    await db.flush()
    await db.refresh(site_config)
    return {"homepage_rotation": site_config.homepage_rotation}
