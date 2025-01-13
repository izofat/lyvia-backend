import typing as t

from lyvia_backend.redis.base import RedisClient
from settings import EMAIL_CODE_EXPIRATION_DELTA


class AuthRedisClient:
    _client = RedisClient.get_client()

    @classmethod
    def set_email_code(cls, email: str, code: str):
        cls._client.set(f"email_code:{email}", code, ex=EMAIL_CODE_EXPIRATION_DELTA)

    @classmethod
    def get_email_code(cls, email: str) -> t.Optional[str]:
        code = t.cast(t.Optional[bytes], cls._client.get(f"email_code:{email}"))
        if not code:
            return None

        return code.decode("utf-8")

    @classmethod
    def delete_email_code(cls, email: str):
        cls._client.delete(f"email_code:{email}")

    @classmethod
    def get_all_email_codes(cls) -> t.Dict[str, str]:
        keys = t.cast(t.List[bytes], cls._client.keys("email_code:*"))
        codes: t.Dict[str, str] = {}
        for key in keys:
            code = t.cast(t.Optional[bytes], cls._client.get(key))
            if not code:
                continue

            key_encoded = key.decode("utf-8")
            email = key_encoded.split(":")[1]
            codes[email] = code.decode("utf-8")

        return codes
