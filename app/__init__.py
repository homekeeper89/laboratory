import os
from flask import Flask
from .config import config
from flasgger import Swagger
from .utils.swagger import get_swagger_config
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from app.core.database import db, migrate


socketio = SocketIO()


def create_app(env: str = "dev") -> Flask:
    app = Flask(__name__)

    app.config.from_object(config[env])
    print(f"RUN {env}")
    with app.app_context():
        JWTManager(app)
        from app.domains import main_api

        app.register_blueprint(main_api)

        Swagger(app, **get_swagger_config())
        db.init_app(app)
        migrate.init_app(app, db)
        socketio.init_app(app)

    @app.route("/")
    def health_check():
        env = os.getenv("FLASK_ENV", "empty")
        return f"env:{env} SUCCESS"

    return app
