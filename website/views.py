#main url per far funzionare il tutto
#min 14
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/') #17,14
def home():
    return "<h1>Test</h1>"

