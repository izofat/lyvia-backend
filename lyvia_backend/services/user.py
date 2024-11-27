import typing as t
from datetime import UTC, datetime, timedelta

import jwt

from lyvia_backend.db.query import Query
from lyvia_backend.exceptions import user as exceptions
from lyvia_backend.logger import Logger
from lyvia_backend.models.db.user import JWTDecoded, JWTEncoded, User
from lyvia_backend.models.response.user import UserSuccessfullResponse
from settings import JWT_SECRET


class UserService:
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

        return cls.login_user(user.username, user.password)

    @classmethod
    def login_user(
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

        token, exp = cls.generate_jwt_token(user)

        return UserSuccessfullResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            lastName=user.lastName,
            email=user.email,
            jwtToken=token,
            exp=exp,
        ).model_dump()

    @classmethod
    def generate_jwt_token(cls, user: User) -> t.Tuple[str, datetime]:
        token_record = cls.query.get_token(user.id)

        if (
            token_record
            and (token_record := token_record[0])
            and token_record["jwtExpireDate"].replace(tzinfo=UTC) - datetime.now(UTC)
            > timedelta(hours=1)
        ):
            return token_record["jwtToken"], token_record["jwtExpireDate"]

        token: JWTEncoded = User.create_token()

        cls.query.insert_token(user.id, token.jwtToken, token.expireDate)

        return token.model_dump()

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
