from typing import Optional

import redis

from settings import RedisConfig


class RedisClient:
    _client: Optional[redis.Redis] = None

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT)
        return cls._client
