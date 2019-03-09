from contextlib import contextmanager
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

db = None
app = None
def create_app(config):
    global app
    global db
    app = Flask(__name__)
    app.config.from_object(config)

    db = SQLAlchemy(app)
    register_blueprints(app)
    return app

@contextmanager
def create_app_context(config):
    """Yield the app, used for testing"""
    app = create_app(config)
    yield app

def register_blueprints(app):
    """Register the blueprints"""
    #have to import to get order proper for db to be initialized :(
    from .blueprints import calls, index

    blueprints = [calls, index]
    for bp in blueprints:
        app.register_blueprint(bp)