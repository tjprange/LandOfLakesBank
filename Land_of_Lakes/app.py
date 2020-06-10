from flask import Flask

from .routes.main import main
from .routes.add import add


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Secret Key'

    # These work as route templates and allow us to organize routes into
    # different files
    app.register_blueprint(main)
    app.register_blueprint(add)

    return app
