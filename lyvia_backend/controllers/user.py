from flask import jsonify, make_response, request
from pydash import get

from lyvia_backend.exceptions import user as user_exceptions
from lyvia_backend.logger import Logger
from lyvia_backend.middleware.validation import validate_field
from lyvia_backend.services.user import UserService


class UserController:
    @staticmethod
    @validate_field("username", "password", "name", "lastName", "email")
    def register():
        try:
            data = request.json
            username = get(data, "username")
            password = get(data, "password")
            name = get(data, "name")
            last_name = get(data, "lastName")
            email = get(data, "email")

            response = UserService.create_user(
                username, password, name, last_name, email
            )

            return make_response(jsonify(response), 201)
        except (
            user_exceptions.UserAlreadyExists,
            user_exceptions.PasswordNotContainsLetter,
            user_exceptions.PasswordNotContainsNumber,
            user_exceptions.PasswordNotContainsSymbol,
            user_exceptions.PasswordTooLong,
            user_exceptions.PasswordTooShort,
            user_exceptions.UsernameTooLong,
            user_exceptions.UsernameTooShort,
        ) as e:
            return make_response(jsonify({"error": e.message}), e.status_code)
        except Exception as e:
            Logger.error("Error while creating user", e)
            return make_response(jsonify({"error": "Internal server error"}), 500)

    @staticmethod
    @validate_field("username", "password")
    def login():
        try:
            data = request.json
            username = get(data, "username")
            password = get(data, "password")

            response = UserService.authenticate_user(username, password)

            return make_response(jsonify(response), 200)
        except (user_exceptions.InvalidCredentials,) as e:
            return make_response(jsonify({"error": e.message}), e.status_code)
        except Exception as e:
            Logger.error("Error while logging in", e)
            return make_response(jsonify({"error": "Internal server error"}), 500)
