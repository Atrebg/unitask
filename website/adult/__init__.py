from flask import Blueprint

adults = Blueprint('adults', __name__)  # passo il nome della mia blueprint

from website.adult import routes
