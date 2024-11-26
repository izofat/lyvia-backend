from flask import Blueprint

from lyvia_backend.controllers.user import UserController

user_bp = Blueprint("user", __name__)

user_bp.route("/register", methods=["POST"])(UserController.register_user)
user_bp.route("/login", methods=["POST"])(UserController.login_user)
