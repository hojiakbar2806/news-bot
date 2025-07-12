from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.config.settings import settings


def get_read_more_button(news_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 To‘liq o‘qish",
                    url=f"https://t.me/{settings.BOT_USERNAME}?start={news_id}"
                )
            ]
        ]
    )
