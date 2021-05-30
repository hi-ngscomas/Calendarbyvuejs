# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect,CSRFError
from requests.api import request
import logging
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home','admin','jackpot','api'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()
    def check_csrf():
        if not is_oauth(request):
            csrf.protect()
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('page-404.html', reason=e.description), 404
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
        

def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    csrf.init_app(app)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app

