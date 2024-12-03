from flask import Blueprint

from lyvia_backend.api.controllers.auth import login, register, verify_email

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/verify-email", methods=["POST"])(verify_email)
