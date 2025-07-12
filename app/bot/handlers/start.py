from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.config.telethon import tg_client
from telethon.tl.custom.message import Message

from app.utils.cache import save_chat_id

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    save_chat_id(message.chat.id)
    await message.answer("✅ Bot ishga tushdi! Sizning chat_id saqlandi.")


@router.channel_post(Command("start"))
async def cmd_start(message: Message):
    save_chat_id(message.chat.id)
    await message.answer("✅ Bot ishga tushdi!")
