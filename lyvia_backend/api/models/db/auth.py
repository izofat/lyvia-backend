from datetime import UTC, datetime

import bcrypt
import jwt
from pydantic import BaseModel, Field, field_validator

from lyvia_backend.api.exceptions import auth as exceptions
from settings import JWT_ALGORITHM, JWT_EXPIRATION_DELTA, JWT_SECRET


class JWTEncoded(BaseModel):
    userId: int
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

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if len(username) < 6:
            raise exceptions.UsernameTooShort()
        if len(username) > 20:
            raise exceptions.UsernameTooLong()
        return username

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise exceptions.PasswordTooShort()
        if len(password) > 100:
            raise exceptions.PasswordTooLong()
        if not any(c.isdigit() for c in password):
            raise exceptions.PasswordNotContainsNumber(
                "Password must contain at least one number"
            )
        if not any(c.isalpha() for c in password):
            raise exceptions.PasswordNotContainsLetter(
                "Password must contain at least one letter"
            )
        if not any(not c.isalnum() for c in password):
            raise exceptions.PasswordNotContainsSymbol(
                "Password must contain at least one symbol"
            )
        return password

    def hash_password(self):
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def decrypt_password(self, decrypted_password: str):
        return bcrypt.checkpw(decrypted_password.encode(), self.password.encode())

    def create_token(self) -> JWTEncoded:
        now = datetime.now(UTC)
        expire_date = now + JWT_EXPIRATION_DELTA
        payload = {"user_id": self.id, "exp": expire_date, "iat": now}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return JWTEncoded(userId=self.id, jwtToken=token, expireDate=expire_date)
