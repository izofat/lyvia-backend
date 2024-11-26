from flask import Flask

from lyvia_backend.routes.user import user_bp
from settings import API_PORT, DEBUG

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(user_bp, url_prefix="/user")

    app.run(port=API_PORT, debug=DEBUG)
