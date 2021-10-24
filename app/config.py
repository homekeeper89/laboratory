import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "SECRET")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWT-SECRET")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "mysql+mysqlconnector://root:root@my_sql:5678/local_dev"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class ProductionConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "prod"
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "dev"
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {"test": TestConfig, "dev": DevelopmentConfig, "prod": ProductionConfig}
