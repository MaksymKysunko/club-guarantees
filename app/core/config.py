from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./club.db"
    SECRET_KEY: str = "dev"

settings = Settings()
