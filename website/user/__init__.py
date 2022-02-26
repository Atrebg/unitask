from flask import Blueprint

users = Blueprint('users', __name__)

from website.user import routes
