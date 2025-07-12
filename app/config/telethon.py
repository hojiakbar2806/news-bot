from telethon import TelegramClient

from app.config.settings import settings


tg_client = TelegramClient(
    "telethon_session",
    settings.TELETHON_API_ID,
    settings.TELETHON_API_HASH,
)
