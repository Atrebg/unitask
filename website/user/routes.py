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


@users.route('/writereview/<task_id>', methods=['GET', 'POST'])
@login_required
def writereview(task_id):
    if request.method == 'POST':
        form = ReviewForm()
        title = form.reviewtitle.data
        description = form.reviewdescription.data
        date = datetime.now()

        t = Offer.query.filter(Offer.id == task_id).first()
        if current_user.type == 'adult':
            t.isPerf = True
            new_review = Review(title=title, text=description, date=date, id_reviewer=current_user.id,
                                id_reviewed=t.scelta,
                                task_id=t.id)
        # aggiungere reviews all'user
        else:
            t.isClosed = True
            new_review = Review(title=title, text=description, date=date, id_reviewer=current_user.id,
                                id_reviewed=t.id_adult,
                                task_id=t.id)
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('views.home'))

    else:
        form = ReviewForm()
        t = Offer.query.filter(Offer.id == task_id).first()
        return render_template("user/review.html", user=current_user, taskscelta=t, form=form)


@users.route('/showreviews/<user_id>/<task_id>', methods=['GET', 'POST'])
@login_required
def showreviews(user_id, task_id):
    if current_user.type == 'adult':
        reviewed = User.query.filter(User.id == user_id).first()
        var = current_user.reviewsreceived
        recensioni = Review.query.filter(Review.id_reviewed == user_id).all()
        return render_template("user/listofreview.html", user=current_user, recensioni=recensioni, reviewed=reviewed,
                               task_id=task_id)
    else:
        reviewed = User.query.filter(User.id == user_id).first()
        recensioni = Review.query.filter(Review.id_reviewed == user_id).all()
        return render_template("user/listofreview.html", user=current_user, recensioni=recensioni, reviewed=reviewed,
                               task_id=0)


@users.route('/about_us')
def about_us():
    return render_template("about_us.html", user=current_user)


@users.route('/account')
def account():
    return render_template("User/account.html", user=current_user)

@users.route('/posttask')
def posttask():
    return render_template("User/posttask.html", user=current_user)

@users.route('/listapplications')
def listapplications():
    return render_template("User/listapplications.html", user=current_user)


@users.route('/personalreviews')
def personalreviews():
    return render_template("User/personalreviews.html", user=current_user)


@users.route("/updateaccount", methods=['GET', 'POST'])
@login_required
def updateaccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Succesfully updated informations', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
    # manca il render template capire cosa serve
    return render_template(user=current_user, form=form)


@users.route('/task/<task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    if current_user.type == 'student':
        t = Offer.query.filter(Offer.id == task_id).first()
        # controllo se ho gia applicato cosi so se posso far comparire il bottone oppure no
        btn = True
        if current_user in t.applicants:
            btn = False
        return render_template("Student/task.html", user=current_user, taskscelta=t, btn=btn)
    else:
        t = Offer.query.filter(Offer.id == task_id).first()
        return render_template("adult/chooseStud.html", user=current_user, taskscelta=t)

