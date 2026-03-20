from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENVIRONMENT: str = "dev"
    PROD_SERVER_URL: str = "http://localhost:3001"

    class Config:
        env_file = ".env"

settings = Settings()
