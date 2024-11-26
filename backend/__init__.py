from flask import Flask
from flask_security import Security
from .model import db
from .data import datastore
from .config import DevelopmentConfig
from .resources import api
from flask_cors import CORS
from .views import view
from werkzeug.security import generate_password_hash
from .model import Sponsor, Influencer
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)
    app.security = Security(app, datastore)
    app.register_blueprint(view, url_prefix='/' )
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    with app.app_context():
        init_db(datastore)

    return app

def init_db(datastore):
    db.create_all()

    # Create roles
    datastore.find_or_create_role(name='admin', verified=True, description='Administrator')
    datastore.find_or_create_role(name='sponsor', verified=True, description='Sponsor')
    datastore.find_or_create_role(name='influencer', verified=True, description='Influencer')

    db.session.commit()

    # Create initial users with roles
    admin_user = datastore.find_user(email='admin@email.com')
    if not admin_user:
        admin_user = datastore.create_user(
            email="admin@email.com", 
            password=generate_password_hash("123456"), 
            roles=["admin"], 
            name="ADMIN"
        )
    db.session.commit()
    
login_manager.login_view = "views.user_login"
@login_manager.user_loader
def load_user(user_id):
    return datastore.find_user(user_id)
