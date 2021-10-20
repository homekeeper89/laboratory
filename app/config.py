import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "super-sEcReat"
    JWT_SECRET_KEY = "super-123-power-456"

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@my_sql:5678/local_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "prod"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@my_sql:5678/local_prod"


class DevelopmentConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "dev"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost:3306/practice"


class TestConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {"test": TestConfig, "dev": DevelopmentConfig, "prod": ProductionConfig}
