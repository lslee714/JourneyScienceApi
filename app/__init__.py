from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

db = None

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    global db

    db = SQLAlchemy(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    """Register the blueprints"""
    #have to import to get order proper for db to be initialized :(
    from .blueprints import calls, index

    blueprints = [calls, index]
    for bp in blueprints:
        app.register_blueprint(bp)