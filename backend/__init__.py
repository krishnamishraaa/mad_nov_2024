from flask import Flask
from flask_security import Security
from .model import db
from .data import datastore
from .config import DevelopmentConfig
from .resources import api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    app.security = Security(app, datastore)
    CORS(app)


    with app.app_context():
        init_db(datastore)
    return app

def init_db(datastore):
    db.create_all()
    datastore.find_or_create_role(name='admin',verified=True, description='Administrator')
    # datastore.create_role(name='user', description='User')
    db.session.commit()
    if not datastore.find_user(email = 'admin@email.com'):
        datastore.create_user(email = "admin@email.com", password = "123456" , roles=["admin"])

    db.session.commit()