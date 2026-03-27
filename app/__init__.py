import os
import tempfile

from flask import Flask

from .models import init_db
from .routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"

    # Vercel is serverless; the repo directory may be read-only and not
    # persistent between requests. Use a writable temp path when deployed.
    db_path = os.environ.get("DATABASE_PATH")
    is_vercel = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))
    if not db_path:
        if is_vercel:
            db_path = os.path.join(tempfile.gettempdir(), "database.db")
        else:
            db_path = "database.db"
    app.config["DATABASE"] = db_path

    init_db(app.config["DATABASE"])
    register_routes(app)
    return app
