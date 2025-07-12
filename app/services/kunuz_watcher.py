import os
from aiogram.types import FSInputFile
from telethon import events
from telethon.tl.types import MessageMediaPhoto

from app.config.telethon import tg_client
from app.bot.instance import bot
from app.utils.cache import get_chat_ids


async def watch_kunuz(chat: str):
    @tg_client.on(events.NewMessage(chats=chat))
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
    print(f"✅ {chat} kuzatilyapti...")
    await tg_client.run_until_disconnected()
