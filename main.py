import os
from dotenv import load_dotenv

env = os.getenv("FLASK_ENV", "dev")
load_dotenv(f".env.{env}")

from app import create_app, socketio

if __name__ == "__main__":
    app = create_app(env)
    socketio.run(app, port=5000)
