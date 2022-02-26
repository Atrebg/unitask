from flask import Blueprint

adults = Blueprint('adults', __name__)

from website.adult import routes
