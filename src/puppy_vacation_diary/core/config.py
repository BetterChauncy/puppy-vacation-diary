from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "小狗的度假日记"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/demo1"

    upload_dir: str = "uploads"
    max_upload_size: int = 50 * 1024 * 1024
    max_files_per_batch: int = 10
    thumbnail_size: int = 400

    storage_backend: str = "local"
    s3_endpoint_url: str | None = None
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_bucket_name: str | None = None
    s3_region: str | None = None

    cors_origins: str = "http://localhost:5173"

    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 30

    wechat_appid: str = ""
    wechat_secret: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
