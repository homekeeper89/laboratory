import os
from app import create_app, socketio

if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "dev")
    app = create_app(env)
    socketio.run(app, host="0.0.0.0", port=5000)
