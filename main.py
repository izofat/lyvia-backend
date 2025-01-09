from flask import Flask

from lyvia_backend.api.routes.auth import auth_bp
from settings import API_PORT, DEBUG, IS_GLOBAL_API

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    # 0.0.0.0 allows external access, 127.0.0.1 is localhost only
    host = "0.0.0.0" if IS_GLOBAL_API else "127.0.0.1"
    app.run(port=API_PORT, debug=DEBUG, host=host)
