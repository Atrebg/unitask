import json

from flask import Blueprint, render_template, flash, jsonify, request, url_for, redirect
from flask_login import login_required, current_user
from datetime import date, datetime
import googlemaps
import requests
from werkzeug.security import generate_password_hash

from website.form import *
from website.models import *
from website.adult import *
from website.views import *
from website.student import *
from website.user import *

API_KEY = "AIzaSyDLAnxto2DehvN5I5YdJuyBgEj7CZnX01A"
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'


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


@students.route('/apply/<task_id>', methods=['GET', 'POST'])
@login_required
def sendapplication(task_id):
    task = Offer.query.filter(Offer.id == task_id).first()
    if not current_user.controlapplication(task):
        flash('You already apply for this task', category='error')
        return redirect(url_for('views.home'))
    task.applicants.append(current_user)
    db.session.commit()
    return redirect(url_for('views.home'))


@students.route('/listapplications', methods=['GET', 'POST'])
@login_required  # every time we go to the home page
def listapplications():
    a = 0
    for off in current_user.getapplicationsopen():
        if not off.isAss:
            a=1
            break

    return render_template("Student/listapplication.html", user=current_user ,a = a )


@students.route('/deleteapplication/<task_id>')
def deleteapplication(task_id):
    t = Offer.query.filter(Offer.id == task_id).first()
    if t.scelta == current_user.id:
        flash('You have been chosen for this task, you cannot delete this task', category='error')
        return redirect(url_for('views.home'))

    t.applicants.remove(current_user)
    db.session.commit()
    flash('Application deleted!', category='success')
    return redirect(url_for('views.home'))


@students.route('/maps')
@login_required
def maps():
    q = Offer.query.filter(Offer.isAss == False, Offer.isClosed == False).all()

    def filtro(t):
        if t.__contains__(current_user):
            return False
        return True

    q1 = filter(filtro, q)

    configurations = {"locations": []}
    for offer in q1:
         configurations["locations"].append(offer.getdict())

    mapsApi = "AIzaSyDLAnxto2DehvN5I5YdJuyBgEj7CZnX01A"
    mapOptions = { "center" : {"lat": 45.1161, "lng": 7.7420}, "fullscreenControl ": True, " mapTypeControl ": False,"streetViewControl": False, "zoom": 2, "zoomControl": True, "maxZoom": 17}
    configurations['mapsApiKey'] = mapsApi
    configurations['mapOptions'] = mapOptions
    return render_template("Student/maps.html", user=current_user, CONFIGURATIONS=configurations, api = mapsApi, mapsOptions=mapOptions)

