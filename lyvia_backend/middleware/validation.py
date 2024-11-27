from functools import wraps

from flask import jsonify, make_response, request
from pydash import get


def validate_field(*required_fields):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.json
            if not data:
                make_response(jsonify({"error": "Missing request body"}), 400)

            missing_fields = [
                field for field in required_fields if not get(data, field)
            ]

            if missing_fields:
                return make_response(
                    jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}),
                    400,
                )

            return f(*args, **kwargs)

        return decorated

    return decorator
