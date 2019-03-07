from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .blueprints import calls

from configs import DebugConfig

db = None

def create_app(config=None):
    app = Flask(__name__)

    config = config or DebugConfig
    app.register_blueprint(calls)
    app.config.from_object(config)

    global db
    db = SQLAlchemy(app)
    return app
