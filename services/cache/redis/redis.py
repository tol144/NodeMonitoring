import redis.asyncio as redis

from typing import Optional

from services.logger import Logger

from config import settings


class RedisCache:
    def __init__(self):
        self._redis = redis.Redis(**settings.redis_config)

    async def ping(self):
        try:
            await self._redis.ping()
            Logger.info("Подключение к Redis установлено")
        except redis.ConnectionError:
            Logger.error("!!! Подключение к Redis не установлено")

    async def set(self,
                  key: str | int,
                  data: dict | str | int,
                  attribute: Optional[str | None] = None,
                  ttl: Optional[int | None] = None):
        if isinstance(data, dict):
            await self.__set_dict(key, data, ttl)
            return

        if attribute is not None:
            await self.__set_dict_attribute(key, data, attribute)
            return

        await self._redis.set(key, data, ex=ttl)

    async def get(self,
                  key: str,
                  attribute: str | None = None) -> dict | str | int | None:
        if await self.__is_dict(key):
            return await self.__get_dict(key, attribute)

        return await self._redis.get(key)

    async def delete(self, key: str):
        # if await self.__is_dict(key):
        #     await self._redis.hdel(key)

        await self._redis.delete(key)

    async def __is_dict(self, key: str) -> bool:
        value_type = await self._redis.type(key)
        if value_type == b'hash':
            return True

        return False

    async def __set_dict(self,
                         key: str | int,
                         data: dict | int,
                         ttl: int | None = None):
        await self._redis.hset(key, mapping=data)
        if ttl is not None:
            await self._redis.expire(key, ttl)

    async def __set_dict_attribute(self,
                                   key: str | int,
                                   data: dict | str | int,
                                   attribute: str):
        if await self._redis.exists(key):
            await self._redis.hset(key, attribute, data)
            return

        await self._redis.hset(key, mapping={attribute: data})

    async def __get_dict(self,
                         key: str | int,
                         attribute: str | None = None) -> dict | str | int | None:
        if attribute is None:
            return await self._redis.hgetall(key)
        else:
            return await self._redis.hget(key, attribute)


redis_cache = RedisCache()
