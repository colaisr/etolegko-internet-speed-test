from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(default="sqlite:///./data/legko.db", alias="DATABASE_URL")
    keitaro_base_url: str = Field(
        default="https://tlgk.host/admin_api/v1",
        alias="KEITARO_BASE_URL",
    )
    keitaro_api_key: str = Field(default="", alias="KEITARO_API_KEY")
    keitaro_default_domain_id: str = Field(default="", alias="KEITARO_DEFAULT_DOMAIN_ID")
    keitaro_default_group_id: str = Field(default="", alias="KEITARO_DEFAULT_GROUP_ID")
    keitaro_default_source_id: str = Field(default="", alias="KEITARO_DEFAULT_SOURCE_ID")
    keitaro_google_redirect_url: str = Field(
        default="https://www.google.com",
        alias="KEITARO_GOOGLE_REDIRECT_URL",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()