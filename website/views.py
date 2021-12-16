#main url per far funzionare il tutto. All the routes are defined here (blueprints allows us)
#min 14

from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #17,14 views is the name of our blueprint (/ is the main page, this function will run
                  # every time we go to the home page
def home():
    return render_template("home.html")

