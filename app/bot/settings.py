import asyncio
from aiogram.types import BotCommand, Message

from app.services.kunuz_watcher import watch_kunuz
from app.utils.logger import logger
from app.bot.instance import bot, dp
from app.config.settings import settings
from app.bot.handlers.news import router as news_router
from app.bot.handlers.start import router as start_router

dp.include_router(start_router)
dp.include_router(news_router)


WEBHOOK_URL = f"{settings.APP_BASE_URL}/webhook"


async def set_bot_commands():
    """Bot buyruqlarini sozlash"""
    commands = [
        BotCommand(command="start", description="🚀 Botni boshlash"),
        BotCommand(command="news", description="📰 Eng yangi yangilik"),
        BotCommand(command="multiple", description="📚 Bir nechta yangilik"),
        BotCommand(command="help", description="❓ Yordam"),
        BotCommand(command="stats", description="📊 Statistika"),
    ]

    await bot.set_my_commands(commands)
    logger.info("Bot buyruqlari o'rnatildi")


async def set_webhook():
    """Webhook sozlash"""
    if settings.BOT_ENV == "webhook":
        await bot.set_webhook(
            WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=["*"]
        )
        logger.info(f"Webhook o'rnatildi: {WEBHOOK_URL}")


async def delete_webhook():
    """Webhook o'chirish"""
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook o'chirildi")


async def run_bot():
    """Botni ishga tushirish"""
    asyncio.create_task(watch_kunuz("@qwerewqwew"))
    asyncio.create_task(watch_kunuz("@kunuzofficial"))

    try:
        # await set_bot_commands()
        await bot.delete_my_commands()

        if settings.BOT_ENV == "polling":
            logger.info("Polling rejimi boshlandi")
            await dp.start_polling(bot)

        elif settings.BOT_ENV == "webhook":
            await set_webhook()
            logger.info("Webhook rejimi boshlandi")
            return dp

    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")
        raise


async def stop_bot():
    """Botni to'xtatish"""
    try:
        if settings.BOT_ENV == "webhook":
            await delete_webhook()
            logger.info("Webhook to'xtatildi")
        await bot.session.close()
        logger.info("Bot to'xtatildi")

    except Exception as e:
        logger.error(f"Bot to'xtatishda xatolik: {e}")
