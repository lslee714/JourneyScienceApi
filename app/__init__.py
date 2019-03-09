from contextlib import contextmanager
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

session = None
app = None
def create_app(config):
    global app
    global session
    app = Flask(__name__)
    app.config.from_object(config)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
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