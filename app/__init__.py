from flask import Flask

from .models import init_db
from .routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["DATABASE"] = "database.db"

    init_db(app.config["DATABASE"])
    register_routes(app)
    return app
