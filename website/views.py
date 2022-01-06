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
    if current_user.type == 'adult':
        Offer.controltasksdate()
        return render_template("Adult/homeAdult.html", user=current_user)
    return redirect(url_for('views.offer'))


@views.route('/offer')
@login_required
def offer():
    q = Offer.query.filter(Offer.isAss == False, Offer.isClosed == False,
                           Offer.applicants.contains(current_user) == False).all()

    return render_template("Student/homeStud.html", user=current_user, tasks=q)


@views.route('/posttask', methods=['GET',
                                   'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def posttask():
    form = PosttaskForm()
    if request.method == 'POST':
        datatask = request.form['date']
        dt = datetime.strptime(datatask, '%Y-%m-%d')
        today = datetime.now()
        if dt < today:
            form.date.data = ''
            flash('La data non puo essere anteriore a quella di oggi', category='error')
            return redirect(url_for('views.posttask'))
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
                return redirect(url_for('views.home'))

    return render_template("Adult/posttask.html", user=current_user, form=form)


@views.route('/task/<task_id>', methods=['GET', 'POST'])
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
        return render_template("Adult/chooseStud.html", user=current_user, taskscelta=t)


@views.route('/apply/<task_id>', methods=['GET', 'POST'])
@login_required
def sendapplication(task_id):
    task = Offer.query.filter(Offer.id == task_id).first()
    if not current_user.controlapplication(current_user, task):
        flash('You already apply for this task', category='error')
        return redirect(url_for('views.home'))
    task.applicants.append(current_user)
    db.session.commit()
    return redirect(url_for('views.home'))
    # daeli = []
    # for task in tasks:
    #   for user in task.applicants:
    #      if user.id == current_user.id:
    #         daeli.append(task)
    # for task in daeli:
    #   tasks.remove(task)


@views.route('/choosestud/<task_id>/<stud_id>', methods=['GET', 'POST'])
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


@views.route('/listapplications', methods=['GET', 'POST'])
@login_required  # every time we go to the home page
def listapplications():
    return render_template("Student/listapplication.html", user=current_user)


@views.route('/writereview/<task_id>', methods=['GET', 'POST'])
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
        return render_template("User/review.html", user=current_user, taskscelta=t, form=form)


@views.route('/showreviews/<user_id>/<task_id>', methods=['GET', 'POST'])
@login_required
def showreviews(user_id, task_id):
    if current_user.type == 'adult':
        reviewed = User.query.filter(User.id == user_id).first()
        var = current_user.reviewsreceived
        recensioni = Review.query.filter(Review.id_reviewed == user_id).all()
        return render_template("User/listofreview.html", user=current_user, recensioni=recensioni, reviewed=reviewed,
                               task_id=task_id)
    else:
        reviewed = User.query.filter(User.id == user_id).first()
        recensioni = Review.query.filter(Review.id_reviewed == user_id).all()
        return render_template("User/listofreview.html", user=current_user, recensioni=recensioni, reviewed=reviewed,
                               task_id=0)


@views.route('/about_us')
def about_us():
    return render_template("about_us.html", user=current_user)


@views.route('/account')
def account():
    return render_template("User/account.html", user=current_user)


@views.route('/taskpending')
def taskpending():
    pending = []
    for task in current_user.tasks:
        if task.isAss:
            pending.append(task)
        if task.isAss == False and task.isPerf == True:
            pending.append(task)

    return render_template("Adult/taskspending.html", user=current_user, pending=pending)


@views.route('/personalreviews')
def personalreviews():
    return render_template("User/personalreviews.html", user=current_user)


@views.route('/deleteapplication/<task_id>')
def deleteapplication(task_id):
    t = Offer.query.filter(Offer.id == task_id).first()
    if t.scelta == current_user.id:
        flash('You have been chosen for this task, you cannot delete this task', category='error')
        return redirect(url_for('views.home'))

    t.applicants.remove(current_user)
    db.session.commit()
    flash('Application deleted!', category='success')
    return redirect(url_for('views.home'))


@views.route('/deletetask/<task_id>')
def deletetask(task_id):
    t = Offer.query.filter(Offer.id == task_id).first()
    if t.applicants:
        flash('There are already applications for this task you cannot delete this task', category='error')
        return redirect(url_for('views.home'))
    db.session.delete(t)
    db.session.commit()
    flash('Task deleted!', category='success')
    return redirect(url_for('views.home'))


@views.route("/account", methods=['GET', 'POST'])
@login_required
def account():
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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template(form=form)



@views.route('/resetdb')
def resetdb():
    db.drop_all()
    db.create_all()
    riempidb()
    return redirect(url_for('auth.logout'))
