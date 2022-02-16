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

API_KEY = "AIzaSyDLAnxto2DehvN5I5YdJuyBgEj7CZnX01A"
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'


@adults.route('/posttask', methods=['GET',
                                    'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def posttask():
    form = PosttaskForm()
    if request.method == 'POST':
        address = request.form['location']
        if not address:
            flash('La data non puo essere anteriore a quella di oggi', category='error')
            return redirect(url_for('adults.posttask'))
        datatask = request.form['date']

        locality = request.form['locality']
        administrative_area_level_1 = request.form['administrative_area_level_1']
        postal_code = request.form['postal_code']
        country = request.form['country']
        dateexpire = request.form['dateexpire']

        dt = datetime.strptime(datatask, '%Y-%m-%d')
        dtexp = datetime.strptime(dateexpire, '%Y-%m-%d')
        params = {
            'key': API_KEY,
            'address': address + locality + administrative_area_level_1 + postal_code + country
        }
        r = requests.get(base_url, params=params).json()
        geometry = r['results'][0]['geometry']['location']
        lat = geometry['lat']
        lng = geometry['lng']
        placeId = r['results'][0]['place_id']

        print(geometry)
        today = datetime.now()
        if dt < today or dtexp < today or dt < dtexp:
            form.date.data = ''
            flash('La data non puo essere anteriore a quella di oggi', category='error')
            return redirect(url_for('adults.posttask'))
        else:
            title = form.tasktitle.data
            description = form.taskdescription.data

            if len(title) < 1:
                flash('Title is too short!', category='error')
            else:
                a = {"title": title, "address1": address, "address2": "Torino", "coords": {"lat": lat, "lng": lng},
                     "placeId": placeId}
                new_offer = Offer(title=title, description=description, date_task=dt, id_adult=current_user.id, lat=lat,
                                  lng=lng, placeId=placeId)
                db.session.add(new_offer)
                db.session.commit()
                flash('Task posted!', category='success')
                return redirect(url_for('views.home'))
    else:
        return render_template("adult/posttask.html", user=current_user, form=form)