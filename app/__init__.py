from flask import Flask
from .config import config


def create_app(env: str = "dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[env])

    @app.route("/ping")
    def temp_ping():
        return "SUCCESS"

    return app
