from datetime import UTC, datetime

import bcrypt
import jwt
from pydantic import BaseModel, Field

from settings import JWT_ALGORITHM, JWT_EXPIRATION_DELTA, JWT_SECRET


class JWTEncoded(BaseModel):
    jwtToken: str
    expireDate: datetime


class JWTDecoded(BaseModel):
    userId: int
    exp: datetime
    iat: datetime


class User(BaseModel):
    id: int = Field(default=1)
    password: str
    username: str
    name: str
    lastName: str
    email: str

    def hash_password(self):
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def decrypt_password(self, decrypted_password: str):
        return bcrypt.checkpw(decrypted_password.encode(), self.password.encode())

    def create_token(self) -> JWTEncoded:
        now = datetime.now(UTC)
        expire_date = now + JWT_EXPIRATION_DELTA
        payload = {"user_id": self.id, "exp": expire_date, "iat": now}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return JWTEncoded(jwtToken=token, expireDate=expire_date)
