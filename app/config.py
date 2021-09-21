import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "super-sEcReat"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@my_sql:5678/local_dev"


class ProductionConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "prod"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@my_sql:5678/local_prod"


class DevelopmentConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "dev"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@127.0.0.1:5678/local_dev"


class TestConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "test"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {"test": TestConfig, "dev": DevelopmentConfig, "prod": ProductionConfig}
