import os
from app import create_app

if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "dev")
    app = create_app(env)
    app.run("0.0.0.0", port=5000)
