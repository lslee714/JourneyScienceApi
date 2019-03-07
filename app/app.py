from flask import Flask

from .blueprints import calls
from .config import DebugConfig


def create_app(config=None):
    app = Flask(__name__)

    #TODO add way to specify configuration, probably a script to run after sourcing env.sh
    config = config or DebugConfig
    app.register_blueprint(calls)
    app.config.from_object(config)
    return app