import os
from app import create_app
from flask_socketio import SocketIO
from app.sockets import register_socket_events

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    app = create_app()
    socketio.run(app, host=host, port=port, debug=debug)