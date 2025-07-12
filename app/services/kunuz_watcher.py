import os
from typing import List, Union
from aiogram import Bot
from aiogram.types import FSInputFile
from telethon import events
from telethon.tl.types import MessageMediaPhoto

from app.config.telethon import tg_client
from app.bot.instance import bot
from app.utils.cache import get_chat_ids


async def watch_kunuz(channel_username: str):
    # Kanal chat_id sini topamiz
    try:
        entity = await tg_client.get_entity(channel_username)
        watching_chat_id = entity.id
    except Exception as e:
        print(f"❌ Kanalni aniqlab bo‘lmadi: {e}")
        return

    @tg_client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        msg = event.message

        if "Реклама" in (msg.text or ""):
            return
        if not isinstance(msg.media, MessageMediaPhoto):
            return

        caption = f"📰 <b>Kun.uz yangilik</b>\n\n{msg.text or ''}"

        try:
            file_path = await msg.download_media()
            photo = FSInputFile(file_path)

            for chat_id in get_chat_ids():
                # O‘zi kuzatayotgan kanalga yuborilmasin
                if int(chat_id) == int(watching_chat_id):
                    continue
                try:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=caption,
                        parse_mode="HTML"
                    )
                except Exception as e:
                    print(f"❌ Xatolik ({chat_id}): {e}")

            os.remove(file_path)

        except Exception as e:
            print(f"❌ Media yuklashda xatolik: {e}")

    await tg_client.start()
    print(f"✅ {channel_username} ({watching_chat_id}) kuzatilyapti...")
    await tg_client.run_until_disconnected()
