import json
from redis.asyncio import Redis
from typing import Optional, Any
from app.config.settings import settings


class RedisClient:
    def __init__(self, url: str , db: int = 0):
        self.redis = Redis.from_url(url, db=db, decode_responses=True)

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0

    async def expire(self, key: str, seconds: int):
        await self.redis.expire(key, seconds)

    async def set_json(self, key: str, value: Any, expire: Optional[int] = None):
        data = json.dumps(value, ensure_ascii=False)
        await self.redis.set(key, data, ex=expire)

    async def get_json(self, key: str) -> Optional[Any]:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def close(self):
        await self.redis.close()




redis = RedisClient(settings.REDIS_URL)