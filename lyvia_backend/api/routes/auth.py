from flask import Blueprint

from lyvia_backend.api.controllers.auth import (
    get_all_email_codes,
    login,
    register,
    send_email_code,
    verify_email,
)

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/verify-email", methods=["POST"])(verify_email)
auth_bp.route("/send-email-code", methods=["POST"])(send_email_code)
auth_bp.route("/get-all-email-codes", methods=["GET"])(get_all_email_codes)
