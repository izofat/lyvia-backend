from lyvia_backend.redis.base import RedisClient
from settings import EMAIL_CODE_EXPIRATION_DELTA


class AuthRedisClient:
    _client = RedisClient.get_client()

    @classmethod
    def set_email_code(cls, email: str, code: str):
        cls._client.set(f"email_code:{email}", code, ex=EMAIL_CODE_EXPIRATION_DELTA)

    @classmethod
    def get_email_code(cls, email: str):
        return cls._client.get(f"email_code:{email}")

    @classmethod
    def delete_email_code(cls, email: str):
        cls._client.delete(f"email_code:{email}")
