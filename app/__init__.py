import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "supergeheimespasswort"  # für flash() & Sessions

    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/uploads")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB Limit
    app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "webp"}
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models import database_models  # dass SQLAlchemy alle Models kennt

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints importieren
    from app.routes.auth import auth_bp
    from .routes.main import main
    from .routes.about import about
    from .routes.projects import projects
    from .routes.contact import contact

    app.register_blueprint(auth_bp)
    app.register_blueprint(main)
    app.register_blueprint(about, url_prefix="/about")
    app.register_blueprint(projects, url_prefix="/projects")
    app.register_blueprint(contact, url_prefix="/contact")

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)


    return app