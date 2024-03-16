from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PAGES_URL: str = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{city}"
    LISTING_URL: str = "https://www.otodom.pl/oferta/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        secrets_dir = "/run/secrets"

    DB_HOST: str = Field(..., env="DB_HOST")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_SCHEMA: str = Field(..., env="DB_SCHEMA")
