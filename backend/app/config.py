"""Environment configuration for local development."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DLR_", env_file=".env", extra="ignore")
    app_name: str = "yaksha"
    database_url: str = "postgresql+psycopg://dlr:dlr_local@localhost:5432/dlr"
