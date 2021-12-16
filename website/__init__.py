#rende il folder eseguibile in python
#ed importabile quando eseguo il main
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'atrebunfigoassurdo'

    from .views import views #We imported the name of the blueprint
    from .auth import auth

    app.register_blueprint(views, url_prefix="/") #Stiamo dicendo come sono definite le pagine e dove sono
    app.register_blueprint(auth, url_prefix="/")


    return app

