from flask import Flask
from flask_cors import CORS

rooms = {}
users = {}

def create_app(config_object=None):
    """Application factory"""

    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)

    CORS(app, origins=["https://sootation.synology.me:8001/", "http://localhost:5173"])

    from . import routes
    app.register_blueprint(routes.api_bp)

    return app