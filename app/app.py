from flask import Flask

from .blueprints import calls

def create_app():
    app = Flask(__name__)
    app.register_blueprint(calls)
    return app