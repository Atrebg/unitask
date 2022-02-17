from flask import Blueprint

students = Blueprint('students', __name__)  # passo il nome della mia blueprint

from website.student import routes
