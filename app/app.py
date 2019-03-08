from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .blueprints import calls, index

from configs import DebugConfig

db = None

def create_app(config=None):
    app = Flask(__name__)

    config = config or DebugConfig
    register_blueprints(app)
    app.config.from_object(config)

    global db
    db = SQLAlchemy(app)
    return app

def register_blueprints(app):
    """Register the blueprints"""
    blueprints = [calls, index]

    for bp in blueprints:
        app.register_blueprint(bp)