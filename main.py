from flask import Flask

from lyvia_backend.api.routes.auth import auth_bp
from settings import API_PORT, DEBUG

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    app.run(port=API_PORT, debug=DEBUG)
