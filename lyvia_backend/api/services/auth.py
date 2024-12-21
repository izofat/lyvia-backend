import secrets
import typing as t
from datetime import UTC, datetime, timedelta

import jwt

from lyvia_backend.api.exceptions import auth as exceptions
from lyvia_backend.api.models.db.auth import JWTDecoded, JWTEncoded, User
from lyvia_backend.api.models.response.auth import UserSuccessfullResponse
from lyvia_backend.db.query import Query
from lyvia_backend.logger import Logger
from lyvia_backend.redis.auth import AuthRedisClient
from settings import JWT_SECRET


class AuthService:
    query = Query()

    @classmethod
    def create_user(
        cls, username: str, password: str, name: str, last_name: str, email: str
    ) -> t.Dict[str, t.Union[str, datetime, int]]:
        user = User(
            username=username,
            password=password,
            name=name,
            lastName=last_name,
            email=email,
        )
        hashed_password = user.hash_password()

        result = cls.query.register_account(
            user.username, hashed_password, user.name, user.lastName, user.email
        )

        if not result:
            raise exceptions.UserAlreadyExists()

        return cls.authenticate_user(user.username, user.password)

    @classmethod
    def authenticate_user(
        cls, username: str, password: str
    ) -> t.Dict[str, t.Union[str, datetime, int]]:
        data = cls.query.get_user(username)

        if not data:
            raise exceptions.InvalidCredentials()

        data = data[0]

        user = User(**data)

        is_pw_matched = user.decrypt_password(password)

        if not is_pw_matched:
            raise exceptions.InvalidCredentials()

        if user.id is None:
            Logger.info("User ID is missing check the data: %s", user.model_dump())
            raise exceptions.InvalidCredentials("User ID is missing")

        token = cls.generate_jwt_token(user)

        return UserSuccessfullResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            lastName=user.lastName,
            email=user.email,
            **token.model_dump(),
        ).model_dump()

    @classmethod
    def generate_jwt_token(cls, user: User) -> JWTEncoded:
        existing_token = cls.query.get_token(user.id)
        existing_token = existing_token[0] if existing_token else None

        if existing_token:
            token_record = JWTEncoded(**existing_token)
            now = datetime.now(UTC)
            time_remaining = token_record.expireDate.replace(tzinfo=UTC) - now
            if time_remaining > timedelta(hours=1):
                return token_record

        token: JWTEncoded = user.create_token()

        cls.query.insert_token(user.id, token.jwtToken, token.expireDate)

        return token

    @classmethod
    def verify_jwt_token(cls, token: str) -> int:
        try:
            decoded_jwt = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            decoded_jwt = JWTDecoded(**decoded_jwt)

            token_data = cls.query.get_token(decoded_jwt.userId)
            token_data = token_data[0]
            encoded_jwt = JWTEncoded(**token_data)

            if token != encoded_jwt.jwtToken:
                raise exceptions.TokenNotMatch()

            return encoded_jwt.userId

        except jwt.ExpiredSignatureError as e:
            raise exceptions.TokenExpired() from e
        except jwt.InvalidTokenError as e:
            raise exceptions.InvalidToken() from e
        except Exception as e:
            Logger.error("Error while verifying jwt token", e)
            raise exceptions.InvalidToken() from e

    @classmethod
    def send_email_code(cls, email: str) -> None:
        cls.query.add_email(email)

        code = "".join(secrets.choice("0123456789") for _ in range(6))
        AuthRedisClient.set_email_code(email, code)

        #! TODO: add smtp email sending here

    @classmethod
    def verify_email(cls, email: str, code: str) -> None:
        saved_code = AuthRedisClient.get_email_code(email)
        if not saved_code:
            raise exceptions.EmailCodeNotFound()

        saved_code = saved_code.decode("utf-8")

        if saved_code != code:
            raise exceptions.InvalidEmailCode()

        cls.query.verify_email(email)
        AuthRedisClient.delete_email_code(email)
