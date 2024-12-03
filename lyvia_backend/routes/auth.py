from flask import Blueprint

from lyvia_backend.controllers.auth import register, login

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)
