# rende il folder eseguibile in python
# ed importabile quando eseguo il main
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import render_template

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'atrebunfigoassurdo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    db.init_app(app)

    from .views import views  # We imported the name of the blueprint
    from .auth import auth
    from website.adult import adults
    from website.student import students
    from website.user import users

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', user='NULL'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html', user='NULL'), 500

    app.register_blueprint(views, url_prefix="/")  # Stiamo dicendo come sono definite le pagine e dove sono
    app.register_blueprint(auth)
    app.register_blueprint(adults)
    app.register_blueprint(students)
    app.register_blueprint(users)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_not_found)

    from .models import User, Offer, Adult, Student

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # dove vogliamo mandare l'user se non loggato
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        # db.drop_all(app=app)
        db.create_all(app=app)
        print('Created Database!')

        # qua ci potrei mettere il popolamento del DB
    else:
        # db.drop_all(app=app)
        db.create_all(app=app)
        print('It already exists')
