from flask import Blueprint

from lyvia_backend.api.controllers.auth import (
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
