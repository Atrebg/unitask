# main url per far funzionare il tutto. All the routes are defined here (blueprints allows us)
# min 14

import json

from flask import Blueprint, render_template, flash, jsonify, request, url_for
from flask_login import login_required, current_user
from datetime import date, datetime

from models import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET',
                           'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def home():
    if request.method == 'POST':
        # mettere if not adult
        print("qui")
        datatask = request.form['dataesecuzione']
        dt = datetime.strptime(datatask, '%Y-%m-%d')
        today = datetime.now()
        if dt < today:
            flash('La data non puo essere anteriore a quella di oggi', category='error')
        else:
            title = request.form.get('title')
            description = request.form.get('description')

            if len(title) < 1:
                flash('Title is too short!', category='error')
            else:
                new_offer = Offer(title=title, description=description, date_task=dt, id_adult=current_user.id)
                db.session.add(new_offer)
                db.session.commit()
                flash('Task posted!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-offer', methods=['POST'])
def delete_offer():
    offer = json.loads(request.data)
    offerId = offer['offerId']
    of = Offer.query.get(offerId)
    if of:
        if of.id_user == current_user.id:
            db.session.delete(of)
            db.session.commit()

    return jsonify({})


@views.route('/offer')
@login_required
def offer():
    tasks = Offer.query.all()  # controllare perche non filtra
    return render_template("offer.html", user=current_user, tasks=tasks)


@views.route('/task/<task_id>', methods=['GET', 'POST'])
@login_required
def taskscelta(task_id):
    if current_user.type == 'student':
        t = Offer.query.filter(Offer.id == task_id).first()
        return render_template("task.html", user=current_user, taskscelta=t)
    else:
        t = Offer.query.filter(Offer.id == task_id).first()
        return render_template("sceltastud.html", user=current_user, taskscelta=t)


@views.route('/apply/<task_id>', methods=['GET', 'POST'])
@login_required
def sendapplication(task_id):
    id_stud = current_user.id
    task = Offer.query.filter(Offer.id == task_id).first()
    task.applicant.append(current_user)
    print(task.applicant)
    db.session.commit()
    tasks = Offer.query.all()  # controllare perche non filtra
    for task in tasks:
        for user in task.applicant:
            if user.id == current_user.id:
                tasks.remove(task)

    return render_template("offer.html", user=current_user, tasks=tasks)


@views.route('/scelta/<task_id>/<stud_id>', methods=['GET', 'POST'])
@login_required
def sceglistud(task_id, stud_id):
    task = Offer.query.filter(Offer.id == task_id).first()
    task.scelta = stud_id
    task.isAss = True
    db.session.commit()
    print("sono qui")
    return render_template("home.html", user=current_user)


@views.route('/sceltarecensione/<task_id>', methods=['GET', 'POST'])
@login_required
def sceltarecensione(task_id):
    t = Offer.query.filter(Offer.id == task_id).first()
    return render_template("review.html", user=current_user, taskscelta=t)


@views.route('/scrivirecensione/<task_id>', methods=['GET', 'POST'])
@login_required
def postareview(task_id):
    if request.method == 'POST':
        titolo = request.form.get('titolo')
        testo = request.form.get('testo')

        t = Offer.query.filter(Offer.id == task_id).first()
        new_review = Review(title=titolo, text=testo, id_reviewer=current_user.id, id_reviewed=t.scelta)
        db.session.add(new_review)
        db.session.commit()
        return render_template("home.html", user=current_user)


@views.route('/vedirecensioni/<stud_id>', methods=['GET', 'POST'])
@login_required
def vedirecensioni(stud_id):
    print stud_id
    stud = User.query.filter(User.id == stud_id).first()
    recensioni = Review.query.filter(Review.id_reviewed == stud_id).all()
    return render_template("vedireview.html", user=current_user, recensioni=recensioni, stud=stud)
