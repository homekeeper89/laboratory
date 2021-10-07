import os
from flask import Flask
from .config import config
from flasgger import Swagger
from .utils import get_swagger_config


def create_app(env: str = "dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[env])

    with app.app_context():
        Swagger(app, template=get_swagger_config())

    @app.route("/ping")
    def temp_ping():
        env = os.getenv("FLASK_ENV", "empty")
        return f"env:{env} SUCCESS"

    return app
