from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Ecodomen data registrator"
    VERSION: str = "0.1"

    API_KEY: str = "apikey"
    API_KEY_HEADER: str = "Authorization"

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "database"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_URI: str | None = None

    @model_validator(mode="after")
    def validator(cls, values: "Settings") -> "Settings":
        values.POSTGRES_URI = (
            f"{values.POSTGRES_USER}:{values.POSTGRES_PASSWORD}@"
            f"{values.POSTGRES_HOST}:{values.POSTGRES_PORT}/{values.POSTGRES_DB}"
        )
        return values


def get_settings():
    return Settings()


settings = get_settings()
