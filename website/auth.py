# Authentication
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .form import LoginForm, SignupForm
from .models import *

auth = Blueprint('auth', __name__)


# We sad clearly that we can accept get and post requests
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #a = 0
    #if a == 1:
     #   riempidb()
     #   return redirect(url_for('views.offer'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.type == 'student':
                    return redirect(url_for('views.offer'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        surname = request.form.get('surName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        type = request.form.get('type')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(surname) < 2:
            flash('Surname must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User
            if type == 'student':
                new_user = Student(email=email, password=generate_password_hash(password1, method='sha256'), first_name=first_name, surname=surname, type=type)
            elif type == 'adult':
                new_user = Adult(email=email, password=generate_password_hash(password1, method='sha256'),
                                 first_name=first_name, surname=surname, type=type)
            else:
                flash('Type errato scrivere student o adult', category='error')
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            if new_user.type == 'student':
                return redirect(url_for('views.offer'))
            
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user, form = form)


def riempidb():
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

    tasks = [
        {'titolo': "cane", 'descrizione': "bla bla bla bla", 'date': "2022-02-16"},
        {'titolo': "gatto", 'descrizione': "bla bla bla bla", 'date': "2022-02-17"},
        {'titolo': "nonna", 'descrizione': "bla bla bla bla", 'date': "2022-02-18"},
        {'titolo': "nonno", 'descrizione': "bla bla bla bla", 'date': "2022-02-19"},
        {'titolo': "spazzatura", 'descrizione': "bla bla bla bla", 'date': "2022-02-19"},
        {'titolo': "trasloco", 'descrizione': "bla bla bla bla", 'date': "2022-02-24"},
        {'titolo': "compiti", 'descrizione': "bla bla bla bla", 'date': "2022-03-28"},
    ]

    ids = {5,6,7,5,6,7,5}

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

    for task in tasks:
            b = 5
            dt = datetime.strptime(task['date'], '%Y-%m-%d')
            us = User.query.get(b)
            b+=1
            new_offer = Offer(title=task['titolo'], description=task['descrizione'], date_task=dt, id_adult=us.id)
            db.session.add(new_offer)
            db.session.commit()

    applicant = User.query.get(1)
    offer1 = Offer.query.get(1)
    offer1.applicants.append(applicant)
    applicant2 = User.query.get(2)
    offer1.applicants.append(applicant2)
    print offer1.applicants
    db.session.commit()





