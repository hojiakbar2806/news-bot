import asyncio
from aiogram.types import Update
from fastapi import APIRouter, Request

from app.config.settings import settings
from app.bot.settings import bot, dp
from app.utils.logger import logger

router = APIRouter()

WEBHOOK_URL = settings.APP_BASE_URL+"/webhook"


@router.post("/webhook")
async def handle_webhook(request: Request):
    try:
        body = await request.body()
        data = Update.model_validate_json(body)
        asyncio.create_task(dp.feed_update(bot, data))
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"[Webhook Error] {e}")
        return {"status": "error", "detail": str(e)}


@router.get("/set_webhook")
async def set_webhook():
    await bot.set_webhook(WEBHOOK_URL)
    return {"status": "ok"}


@router.get("/delete_webhook")
async def delete_webhook():
    await bot.delete_webhook()
    return {"status": "ok"}


@router.get("/get_webhook_info")
async def get_webhook_info():
    return await bot.get_webhook_info()
