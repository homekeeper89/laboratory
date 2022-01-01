import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "SECRET")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWT-SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 12  # 12시간

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "mysql+mysqlconnector://root:root@my_sql:5678/local_dev"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    POLICY = {"LIMIT_USER_COUNTS": 4}


class ProductionConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "prod"
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "dev"
    DEVELOPMENT = True
    DEBUG = True

    DEV_ACCESS_TOKEN = "super_power_token"


class TestConfig(Config):
    ENV = os.environ.get("FLASK_ENV") or "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    DEV_ACCESS_TOKEN = "super_power_token_test"


class LaboratoryConfig(Config):
    ENV = "laboratory"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost:5678/local_dev"


config = {
    "test": TestConfig,
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "lab": LaboratoryConfig,
}
