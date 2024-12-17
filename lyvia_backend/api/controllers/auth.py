from flask import jsonify, make_response, request
from pydash import get

from lyvia_backend.api.exceptions import auth as auth_exceptions
from lyvia_backend.api.middleware.validation import validate_field
from lyvia_backend.api.services.auth import AuthService
from lyvia_backend.logger import Logger


@validate_field("username", "password", "name", "lastName", "email")
def register():
    try:
        data = request.json
        username = get(data, "username")
        password = get(data, "password")
        name = get(data, "name")
        last_name = get(data, "lastName")
        email = get(data, "email")

        response = AuthService.create_user(username, password, name, last_name, email)

        return make_response(jsonify(response), 201)
    except (
        auth_exceptions.UserAlreadyExists,
        auth_exceptions.PasswordNotContainsLetter,
        auth_exceptions.PasswordNotContainsNumber,
        auth_exceptions.PasswordNotContainsSymbol,
        auth_exceptions.PasswordTooLong,
        auth_exceptions.PasswordTooShort,
        auth_exceptions.UsernameTooLong,
        auth_exceptions.UsernameTooShort,
    ) as e:
        return make_response(jsonify({"error": e.message}), e.status_code)
    except Exception as e:
        Logger.error("Error while creating user", e)
        return make_response(jsonify({"error": "Internal server error"}), 500)


@validate_field("username", "password")
def login():
    try:
        data = request.json
        username = get(data, "username")
        password = get(data, "password")

        response = AuthService.authenticate_user(username, password)

        return make_response(jsonify(response), 200)
    except auth_exceptions.InvalidCredentials as e:
        return make_response(jsonify({"error": e.message}), e.status_code)
    except Exception as e:
        Logger.error("Error while logging in", e)
        return make_response(jsonify({"error": "Internal server error"}), 500)


@validate_field("email", "code")
def verify_email():
    try:
        data = request.json
        email = get(data, "email")
        code = get(data, "code")

        AuthService.verify_email(email, code)

        return make_response(jsonify({"Message": "Email verify successful"}), 200)
    except (auth_exceptions.InvalidEmailCode, auth_exceptions.EmailCodeNotFound) as e:
        return make_response(jsonify({"error": e.message}), e.status_code)
    except Exception as e:
        Logger.error("Error while verifying email", e)
        return make_response(jsonify({"error": "Internal server error"}), 500)


@validate_field("email")
def send_email_code():
    try:
        data = request.json
        email = get(data, "email")

        AuthService.send_email_code(email)

        return make_response(jsonify({"Message": "Email code sent"}), 200)
    except Exception as e:
        Logger.error("Error while sending email code", e)
        return make_response(jsonify({"error": "Internal server error"}), 500)
