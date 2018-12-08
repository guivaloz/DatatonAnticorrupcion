from flask import Flask

from dataton_anticorrupcion.blueprints.sistemas import sistemas
from dataton_anticorrupcion.blueprints.usuarios import usuarios
from dataton_anticorrupcion.blueprints.usuarios.models import Usuarios

from dataton_anticorrupcion.blueprints.contrataciones_abiertas import contrataciones_abiertas

from dataton_anticorrupcion.extensions import csrf, db, login_manager, pwd_context


def create_app(settings_override=None):
    """
    Create the Flask app, mutates the app passed in
    """
    # Initialize Flask
    app = Flask(__name__, instance_relative_config=True)
    # Load settings
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    if settings_override:
        app.config.update(settings_override)
    # Register blueprints
    app.register_blueprint(contrataciones_abiertas)
    # Register blueprints
    app.register_blueprint(sistemas)
    app.register_blueprint(usuarios)
    # Extras
    extensions(app)
    authentication(app, Usuarios)
    # Return app
    return app

def extensions(app):
    """
    Register extensions
    """
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    return None

def authentication(app, user_model):
    """
    Initialize the Flask-Login extension
    mutates the app passed in
    """
    login_manager.login_view = 'usuarios.login'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)
