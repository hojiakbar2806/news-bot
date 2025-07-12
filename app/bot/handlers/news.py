from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from app.config.telethon import tg_client
from telethon.tl.custom.message import Message

from app.utils.cache import delete_chat_id

router = Router()


@router.message(Command("stop"))
async def echo(message: Message):
    delete_chat_id(message.chat.id)
    await message.answer("✅ Bot to'xtadi!")


@router.channel_post(Command("stop"))
async def echo(message: Message):
    delete_chat_id(message.chat.id)
    await message.answer("✅ Bot to'xtadi!")