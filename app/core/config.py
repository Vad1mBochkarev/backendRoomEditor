from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MINIO_URL: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "room-editor"
    MINIO_SECURE: bool = False
