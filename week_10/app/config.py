from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="week-10-observability-api", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")
    rate_limit_default: str = Field(default="60/minute", alias="RATE_LIMIT_DEFAULT")
    rate_limit_write: str = Field(default="10/minute", alias="RATE_LIMIT_WRITE")
    rate_limit_external: str = Field(default="5/minute", alias="RATE_LIMIT_EXTERNAL")

    external_service_url: str = Field(
        default="https://httpbin.org/status/200",
        alias="EXTERNAL_SERVICE_URL",
    )
    external_failure_mode: bool = Field(default=False, alias="EXTERNAL_FAILURE_MODE")
    circuit_fail_max: int = Field(default=3, alias="CIRCUIT_FAIL_MAX")
    circuit_reset_timeout_seconds: int = Field(
        default=30,
        alias="CIRCUIT_RESET_TIMEOUT_SECONDS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
