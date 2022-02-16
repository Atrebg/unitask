import json

from flask import Blueprint, render_template, flash, jsonify, request, url_for, redirect
from flask_login import login_required, current_user
from datetime import date, datetime
import googlemaps
import requests
from werkzeug.security import generate_password_hash

from website.form import *

from website.models import *
API_KEY = "AIzaSyDLAnxto2DehvN5I5YdJuyBgEj7CZnX01A"
base_url= 'https://maps.googleapis.com/maps/api/geocode/json?'
adult = Blueprint('adult', __name__)


