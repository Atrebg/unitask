#main url per far funzionare il tutto
#min 14
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #17,14
def home():
    return render_template("home.html")

