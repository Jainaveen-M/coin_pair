from flask import Flask
from src.services.order_service import order_service


def create_app():
    app = Flask(__name__)
    app.register_blueprint(order_service)
    return app
    