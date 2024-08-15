from flask import Flask
from app.routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Register blueprint
    app.register_blueprint(bp)

    return app
