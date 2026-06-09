from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from puppy_vacation_diary.core.config import settings


def create_access_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(days=settings.jwt_expire_days)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
