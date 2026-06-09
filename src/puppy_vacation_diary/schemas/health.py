from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str = "小狗的度假日记"
