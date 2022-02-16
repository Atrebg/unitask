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


@students.route('/offer')
@login_required
def offer():
    Offer.controltasksdate()
    q = Offer.query.filter(Offer.isAss == False, Offer.isClosed == False).all()

    def filtro(t):
        if t.__contains__(current_user):
            return False
        return True

    q1 = filter(filtro, q)

    return render_template("student/homeStud.html", user=current_user, tasks=q1)




