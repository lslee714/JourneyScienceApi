from celery import Celery
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

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URI'])
    celery.conf.update(app.config)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    session = Session()
    register_blueprints(app)
    return app

def register_blueprints(app):
    """Register the blueprints"""
    #have to import to get order proper for db to be initialized :(
    from .blueprints import calls, index

    blueprints = [calls, index]
    for bp in blueprints:
        app.register_blueprint(bp)