from flask import Blueprint

students = Blueprint('students', __name__)

from website.student import routes
