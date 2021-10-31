from flask import current_app
from .schema.socket import data

TITLE = "RUN WITH ME"


def get_swagger_config() -> dict:
    return {
        "config": {
            "openapi": "3.0.2",
            "host": current_app.config.get("HOST_URL"),
            "basePath": "",  # base bash for blueprint registration
            "schemes": current_app.config.get("HOST_PROTOCOL"),
            "operationId": "getmyData",
            "specs": [
                {
                    "endpoint": "apispec",
                    "route": "/apidocs/apispec.json",
                    "rule_filter": lambda rule: True,  # all in
                    "model_filter": lambda tag: True,  # all in
                }
            ],
            "static_url_path": "/apidocs/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/odin/docs",
            "headers": [],
            "components": {
                "schemas": data,
                "securitySchemes": {
                    "userAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "user jwt token 사용",
                    },
                },
            },
        },
        "template": {
            "info": {
                "title": TITLE,
                "description": f"{TITLE} APIDOCS",
                "contact": {
                    "responsibleOrganization": "Me",
                    "responsibleDeveloper": "Me",
                    "email": "homekeeper89@gmail.com",
                },
                "termsOfService": "https://github.com/DDD-6/Reversed-666-server",
                "version": "0.0.1",
            },
        },
    }
