from flask import Flask
from flask import request, session
from flask import render_template, url_for, redirect, flash

from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import config

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "main.login"

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app