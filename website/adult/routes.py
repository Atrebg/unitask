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


@adults.route('/posttask', methods=['GET', 'POST'])
@login_required
def posttask():
    form = PosttaskForm()
    if request.method == 'POST':
        address = request.form['location']
        if not address:
            flash('Insert a valid address', category='error')
            return redirect(url_for('adults.posttask'))
        datatask = request.form['date']
        amount = request.form['amount']

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
        today = datetime.now()
        if dt < today or dtexp < today or dt < dtexp:
            form.date.data = ''
            flash('The date inserted cannot be before the current date', category='error')
            return redirect(url_for('adults.posttask'))
        else:
            title = form.tasktitle.data
            description = form.taskdescription.data

            if len(title) < 1:
                flash('Title is too short!', category='error')
            else:
                a = {"title": title, "address1": address, "address2": "Torino", "coords": {"lat": lat, "lng": lng},
                     "placeId": placeId}
                new_offer = Offer(title=title, description=description, date_task=dt, dateexpire=dtexp,
                                  id_adult=current_user.id, lat=lat,
                                  lng=lng, placeId=placeId, amount=amount, address=address)
                db.session.add(new_offer)
                db.session.commit()
                flash('Task posted!', category='success')
                return redirect(url_for('views.home'))
    else:
        return render_template("adult/posttask.html", user=current_user, form=form)


@adults.route('/choosestud/<task_id>/<stud_id>', methods=['GET', 'POST'])
@login_required
def choosestud(task_id, stud_id):
    task1 = Offer.query.filter(Offer.id == task_id).first()
    if not Offer.controldate(task1):
        flash('Too late the task is closed', category='error')
        return redirect(url_for('views.home'))
    task1.scelta = stud_id
    task1.isAss = True
    db.session.commit()

    return redirect(url_for('views.home'))


@adults.route('/taskpending')
def taskpending():
    pending = []
    for task in current_user.tasks:
        if task.isAss and task.isClosed == False:
            pending.append(task)
        if task.isAss == False and task.isPerf == True:
            pending.append(task)

    return render_template("adult/taskspending.html", user=current_user, pending=pending)


@adults.route('/deletetask/<task_id>')
def deletetask(task_id):
    t = Offer.query.filter(Offer.id == task_id).first()
    if t.applicants:
        flash('There are already applications for this task you cannot delete this task', category='error')
        return redirect(url_for('views.home'))
    db.session.delete(t)
    db.session.commit()
    flash('Task deleted!', category='success')
    return redirect(url_for('views.home'))
