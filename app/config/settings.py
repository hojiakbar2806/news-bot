from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str
    APP_BASE_URL: str

    BOT_ENV: str
    BOT_TOKEN: str

    TELETHON_API_ID: str
    TELETHON_API_HASH: str

    BOT_USERNAME: str = "@dastur_hn_bot"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
