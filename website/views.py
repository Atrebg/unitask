# main url per far funzionare il tutto. All the routes are defined here (blueprints allows us)
# min 14

import json

from flask import Blueprint, render_template, flash, jsonify, request, url_for, redirect
from flask_login import login_required, current_user
from datetime import date, datetime

from .auth import riempidb
from .form import *

from models import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET',
                           'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def home():
    today=datetime.today()
    stamp =[]
    for task in current_user.tasks:
        if task.date_task>today:
            stamp.append(task)
        else:
            task.isPerf = True
            db.session.commit()

    return render_template("home.html", user=current_user, tasks=stamp)


@views.route('/posttask', methods=['GET',
                                   'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def posttask():
    form = PosttaskForm()
    if request.method == 'POST':
        # mettere if not adult

        datatask = request.form['date']
        dt = datetime.strptime(datatask, '%Y-%m-%d')
        today = datetime.now()
        if dt < today:
            flash('La data non puo essere anteriore a quella di oggi', category='error')
        else:
            title = form.tasktitle.data
            description = form.taskdescription.data

            if len(title) < 1:
                flash('Title is too short!', category='error')
            else:
                new_offer = Offer(title=title, description=description, date_task=dt, id_adult=current_user.id)
                db.session.add(new_offer)
                db.session.commit()
                flash('Task posted!', category='success')

    return render_template("posttask.html", user=current_user, form=form)


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
    tasks = Offer.query.all()
    u = current_user
    daeli = []
    for task in tasks:
        if task.isAss == False:
            for stud in task.applicants:
                if stud.id == current_user.id:
                    daeli.append(task)
        else:
            daeli.append(task)
    for task in daeli:
        tasks.remove(task)

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
    task.applicants.append(current_user)
    print(task.applicants)
    db.session.commit()
    tasks = Offer.query.all()
    daeli = []
    for task in tasks:
        for user in task.applicants:
            if user.id == current_user.id:
                daeli.append(task)
    for task in daeli:
        tasks.remove(task)

    return render_template("offer.html", user=current_user, tasks=tasks)


@views.route('/scelta/<task_id>/<stud_id>', methods=['GET', 'POST'])
@login_required
def sceglistud(task_id, stud_id):
    task = Offer.query.filter(Offer.id == task_id).first()
    task.scelta = stud_id
    task.isAss = True
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/listapplications', methods=['GET', 'POST'])
@login_required  # every time we go to the home page
def listapplications():
    return render_template("listapplication.html", user=current_user)


@views.route('/sceltarecensione/<task_id>', methods=['GET', 'POST'])
@login_required
def sceltarecensione(task_id):
    if request.method == 'POST':
        form = ReviewForm()
        title = form.reviewtitle.data
        description = form.reviewdescription.data
        date = datetime.now()

        t = Offer.query.filter(Offer.id == task_id).first()
        if current_user.type == 'adult':
            t.isPerf = True
        #aggiungere reviews all'user
        new_review = Review(title=title, text=description, date=date, id_reviewer=current_user.id, id_reviewed=t.scelta, task_id=t.id)
        db.session.add(new_review)
        db.session.commit()
        if current_user.type == 'adult':
            return render_template("home.html", user=current_user)
        else:
            return render_template("listapplication.html", user=current_user)
    else:
        form = ReviewForm()
        t = Offer.query.filter(Offer.id == task_id).first()
        return render_template("review.html", user=current_user, taskscelta=t, form=form)


@views.route('/vedirecensioni/<stud_id>', methods=['GET', 'POST'])
@login_required
def vedirecensioni(stud_id):
    print stud_id
    stud = User.query.filter(User.id == stud_id).first()
    recensioni = Review.query.filter(Review.id_reviewed == stud_id).all()
    return render_template("vedireview.html", user=current_user, recensioni=recensioni, stud=stud)


@views.route('/about_us')
def about_us():
    return render_template("about_us.html", user=current_user)


@views.route('/account')
def account():
    return render_template("account.html", user=current_user)


@views.route('/taskpending')
def taskpending():
    pending = []
    for task in current_user.tasks:
        if task.isAss:
            pending.append(task)
        if task.isAss == False and task.isPerf == True:
            pending.append(task)

    return render_template("taskspending.html", user=current_user, pending=pending)


@views.route('/resetdb')
def resetdb():
    db.drop_all()
    db.create_all()
    riempidb()
    return redirect(url_for('auth.logout'))
