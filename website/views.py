# main url per far funzionare il tutto. All the routes are defined here (blueprints allows us)
# min 14

import json

from flask import Blueprint, render_template, flash, jsonify, request
from flask_login import login_required, current_user

from models import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET',
                           'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if len(title) < 1:
            flash('Title is too short!', category='error')
        else:
            new_offer = Offer(title=title, description=description, id_poster=current_user.id)
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
        if of.id_poster == current_user.id:
            db.session.delete(of)
            db.session.commit()

    return jsonify({})


@views.route('/offer')
@login_required
def offer():
    tasks = Offer.query.filter(Offer.id_user!=current_user.id).all()  # controllare perche non filtra
    return render_template("offer.html", user=current_user, tasks=tasks)


@views.route('/task/<task_id>', methods=['GET', 'POST'])
@login_required
def taskscelta(task_id):
    t = Offer.query.filter(Offer.id == task_id).first()
    return render_template("task.html", user=current_user, taskscelta=t)


def sendapplycation(task_id):
    if request.method == 'POST':
        return render_template("home.html", user=current_user)
