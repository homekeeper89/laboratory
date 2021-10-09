TITLE = "RUN WITH ME"


def get_swagger_config() -> dict:
    return {
        "openapi": "3.0",
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
        "host": "TBD",  # overrides localhost:500
        "basePath": "",  # base bash for blueprint registration
        "schemes": ["http", "https"],
        "operationId": "getmyData",
    }
