from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

rooms = {}
users = {}
allowed_origins=["https://sootation.synology.me:8001", "http://localhost:5173"]

socketio = SocketIO(cors_allowed_origins=allowed_origins)

def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)

    CORS(app, origins=allowed_origins)

    from . import routes
    app.register_blueprint(routes.api_bp)

    socketio.init_app(app)
    from .sockets import register_socket_events
    register_socket_events(socketio)

    return app