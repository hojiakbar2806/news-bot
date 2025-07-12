from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.bot.settings import run_bot, stop_bot
from app.scheduler.setup import setup_scheduler
from app.utils.logger import setup_logger, logger
from app.routes.webhook import router as webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup_logger()
    await run_bot()
    # await setup_scheduler()
    logger.info(f"FastAPI started [mode: {settings.APP_ENV}]")
    yield
    await stop_bot()
    logger.info("FastAPI stopped")

app = FastAPI(
    title="Uzum Bot",
    description="Uzum Bot",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(webhook_router)


@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "FastAPI is running"}
