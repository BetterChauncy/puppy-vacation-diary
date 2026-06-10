import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from puppy_vacation_diary.core.auth import create_access_token
from puppy_vacation_diary.core.config import settings
from puppy_vacation_diary.core.dependencies import get_current_user, get_db
from puppy_vacation_diary.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


class WxLoginRequest(BaseModel):
    code: str


class WxLoginResponse(BaseModel):
    token: str
    user_id: int
    is_new: bool


class UserResponse(BaseModel):
    id: int
    nickname: str | None = None
    avatar: str | None = None


async def _get_or_create_user(db: AsyncSession, openid: str) -> tuple[User, bool]:
    result = await db.execute(select(User).where(User.openid == openid))
    user = result.scalar_one_or_none()
    if user:
        return user, False
    user = User(openid=openid)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user, True


async def _wx_code_to_openid(code: str) -> str:
    if not settings.wechat_appid or not settings.wechat_secret:
        logger.warning("WECHAT_APPID or WECHAT_SECRET not set, using mock openid")
        return f"mock_openid_{code[:16]}"
    try:
        async with httpx.AsyncClient(verify=False, timeout=15) as client:
            resp = await client.get(
                "https://api.weixin.qq.com/sns/jscode2session",
                params={
                    "appid": settings.wechat_appid,
                    "secret": settings.wechat_secret,
                    "js_code": code,
                    "grant_type": "authorization_code",
                },
            )
            data = resp.json()
            if "openid" not in data:
                logger.error("wx jscode2session failed: %s", data)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"wx login failed: {data}")
            return data["openid"]
    except httpx.TimeoutException:
        logger.error("wx jscode2session timed out")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="wx jscode2session timed out")
    except httpx.RequestError as e:
        logger.error("wx jscode2session request failed: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"wx jscode2session failed: {e}")


@router.post("/auth/wx-login", response_model=WxLoginResponse)
async def wx_login(data: WxLoginRequest, db: AsyncSession = Depends(get_db)):
    openid = await _wx_code_to_openid(data.code)
    user, is_new = await _get_or_create_user(db, openid)
    token = create_access_token(user.id)
    return WxLoginResponse(token=token, user_id=user.id, is_new=is_new)


@router.put("/auth/profile", response_model=UserResponse)
async def update_profile(
    profile: UserResponse,
    user: User | None = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if profile.nickname is not None:
        user.nickname = profile.nickname
    if profile.avatar is not None:
        user.avatar = profile.avatar
    await db.flush()
    await db.refresh(user)
    return user


@router.get("/auth/me", response_model=UserResponse)
async def get_me(user: User | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user
