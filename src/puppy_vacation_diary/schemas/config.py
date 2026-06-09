from pydantic import BaseModel


class ConfigUpdate(BaseModel):
    homepage_rotation: str
