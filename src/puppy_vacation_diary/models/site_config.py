from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from puppy_vacation_diary.models.base import Base


class SiteConfig(Base):
    __tablename__ = "site_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    homepage_rotation: Mapped[str] = mapped_column(String(10), default="daily")
