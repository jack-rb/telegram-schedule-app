from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./schedule.db"
    BOT_TOKEN: str = "your_bot_token_here"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    DOMAIN: str = "localhost:8000"
    SUBDOMAIN_ENABLED: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
