# rende il folder eseguibile in python
# ed importabile quando eseguo il main
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'atrebunfigoassurdo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views  # We imported the name of the blueprint
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")  # Stiamo dicendo come sono definite le pagine e dove sono
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Offer, Review

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # dove vogliamo mandare l'user se non loggato
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        # qua ci potrei mettere il popolamento del DB