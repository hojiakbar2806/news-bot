from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


async def setup_scheduler():

    # scheduler.add_job(
    #     args=[1],
    #     trigger=CronTrigger(hour=23, minute=59),
    # )

    scheduler.start()
