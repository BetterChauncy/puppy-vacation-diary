from fastapi import APIRouter

from puppy_vacation_diary.core.config import settings
from puppy_vacation_diary.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(app_name=settings.app_name)
