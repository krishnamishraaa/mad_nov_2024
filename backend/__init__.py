from flask import Flask
from flask_security import Security
from .model import db
from .data import datastore
from .config import DevelopmentConfig
from .resources import api
from .instances import cache
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from backend.views import view
from backend.admin_views import admin_view
from backend.sponsor_views import sponsor_view
import flask_excel as excel


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.security = Security(app, datastore)
    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(admin_view, url_prefix="/")
    app.register_blueprint(sponsor_view, url_prefix="/")
    CORS(app)
    cache.init_app(app)

    with app.app_context():
        init_db(datastore)

    return app


def init_db(datastore):
    db.create_all()

    # Create roles
    datastore.find_or_create_role(
        name="admin", verified=True, description="Administrator"
    )
    datastore.find_or_create_role(name="sponsor", verified=True, description="Sponsor")
    datastore.find_or_create_role(
        name="influencer", verified=True, description="Influencer"
    )

    db.session.commit()

    # Create initial users with roles
    admin_user = datastore.find_user(email="admin@email.com")
    if not admin_user:
        admin_user = datastore.create_user(
            email="admin@email.com",
            password=generate_password_hash("123456"),
            roles=["admin"],
            name="ADMIN",
        )
