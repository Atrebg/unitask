# main url per far funzionare il tutto. All the routes are defined here (blueprints allows us)
# min 14

import json

import errorhandler as errorhandler
from flask import Blueprint, render_template, flash, jsonify, request, url_for, redirect
from flask_login import login_required, current_user
from datetime import date, datetime
import googlemaps
import requests
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException

from .auth import riempidb
from .form import *
from website.student import *
from website.adult import *
from website.user import *

from models import *

API_KEY = "AIzaSyDLAnxto2DehvN5I5YdJuyBgEj7CZnX01A"
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
views = Blueprint('views', __name__)


@views.route('/', methods=['GET',
                           'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def home():
    if current_user.type == 'adult':
        Offer.controltasksdate()
        for of in current_user.tasks:
            if not of.isClosed:
                print(current_user.tasks)
        for offer in current_user.gettasksopen():
            print (offer)
        return render_template("adult/homeAdult.html", user=current_user)
    return redirect(url_for('students.offer'))


@views.route('/resetdb')
def resetdb():
    db.drop_all()
    db.create_all()
    riempidb()
    return redirect(url_for('auth.logout'))


@views.route('/resetdbusers')
def resetdbuser():
    db.drop_all()
    db.create_all()
    studenti = [
        {'name': "Giacomo", 'surname': "Bertazzolo"},
        {'name': "Valeria", 'surname': "Liuni"},
        {'name': "Samuele", 'surname': "Stasi"},
        {'name': "Oliviero", 'surname': "Vidoni"},
    ]

    adulti = [
        {'name': "mamma", 'surname': "papa"},
        {'name': "zia", 'surname': "zio"},
        {'name': "nonno", 'surname': "nonna"},
    ]

    for studente in studenti:
        mail = studente['name'].lower() + studente['surname'].lower() + '@mail.com'
        user_db = Student(first_name=studente['name'],
                          surname=studente['surname'],
                          email=mail,
                          password=generate_password_hash('1234567890', method='sha256'),
                          type='student')
        db.session.add(user_db)
        db.session.commit()

    for adulto in adulti:
        mail = adulto['name'].lower() + adulto['surname'].lower() + '@mail.com'
        user_db = Adult(first_name=adulto['name'],
                        surname=adulto['surname'],
                        email=mail,
                        password=generate_password_hash('1234567890', method='sha256'),
                        type='adult')
        db.session.add(user_db)
        db.session.commit()

    return redirect(url_for('auth.logout'))



