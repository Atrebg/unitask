# Authentication
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .form import LoginForm, SignupForm
from .models import *

auth = Blueprint('auth', __name__)


# We sad clearly that we can accept get and post requests

@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.type == 'student':
                    return redirect(url_for('views.home'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("User/login.html", user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():

        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        password = request.form.get('password')
        description = request.form.get('description')
        passwordconf = request.form.get('passwordconf')
        type = request.form.get('type')

        user = User.query.filter_by(email=email).first()
        new_user = User
        if type == 'student':
            new_user = Student(email=email, password=generate_password_hash(password, method='sha256'), first_name=name,
                               surname=surname, type=type, description=description)
        elif type == 'adult':
            new_user = Adult(email=email, password=generate_password_hash(password, method='sha256'),
                             first_name=name, surname=surname, type=type, description=description)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', category='success')
        login_user(new_user, remember=True)
        if new_user.type == 'student':
            return redirect(url_for('students.offer'))

        return redirect(url_for('views.home'))
    return render_template("User/sign_up.html", user=current_user, form=form)


def riempidb():
    studenti = [
        {'name': "Giacomo", 'surname': "Bertazzolo",
         'description': "I am a studente in IT engineering. I can help you with your computer and all of your electronic devices."},
        {'name': "Valeria", 'surname': "Liuni",
         'description': "I am a student in Engineering and Management at Politecnico di Torino. I love animals and I am ready to help you with them!"},
        {'name': "Caterina", 'surname': "Nassi",
         'description': "I am a student in Education and Formation. I love babies, and I am usually available at the last minute. "},
        {'name': "Oliviero", 'surname': "Vidoni",
         'description': ""},
    ]

    adulti = [
        {'name': "Maria", 'surname': "Bianchi",
         'description': "I am a Manager in a consultancy firm. I have a 4 lovely dogs and I am always looking for someone who can help me with them."},
        {'name': "Paolo", 'surname': "Giorgi",
         'description': "I am a grandfather with 4 amazing nephews. They cannot bear anymore my problems with technology and for this reason I decided to join this community."},
        {'name': "Mario", 'surname': "Rossi",
         'description': "I am a single father whit 3 beautiful children. It may happen that I cannot find someone who can help me with them, especially when there are last minute calls at work."},
    ]

    tasks = [
        {'titolo': "My lovely pet ",
         'descrizione': "I need help with my lovey pet. I'm looking for someone who can take care of her for the afternoon. She is really sweet and docile.",
         'date': "2022-04-23", 'lat': "45.058427", 'lng': "7.655138", 'placeId': "ChIJbZ33QSFtiEcR3Yr-cxhtfDQ",
         'address': "Corso Lione 40"},
        {'titolo': "My PC is not working",
         'descrizione': "I am looking for someone who can fix my computer. My internet connection does not work, can you help me?",
         'date': "2022-05-17", 'lat': "45.07215960121708", 'lng': "7.681296735921444",
         'placeId': "ChIJ-w5Ey3NtiEcRizrB7W-hDNI", 'address': "Via Barbaroux 20"},
        {'titolo': "My grandmother",
         'descrizione': "I am looking for someone who can keep company to my gradmother because she is very lonely.",
         'date': "2022-05-18", 'lat': "45.0602789482421", 'lng': "7.659934143334852",
         'placeId': "ChIJx4qR9SJtiEcRqjxf1yPr6KI", 'address': "Via Marco Polo 38"},
        {'titolo': "My house is a mess!",
         'descrizione': "Hy everyone! I am looking for someone who can help me with my messy house. I am an artist and I have a lot of things in my house that I want to get rid off. Please come and help me! ",
         'date': "2022-04-19", 'lat': "45.074369423709875", 'lng': "7.6562016089387965",
         'placeId': "ChIJXbcpbQJtiEcRayf8ZeGWbPI", 'address': "Corso Ferrucci 12"},
        {'titolo': "Out of town",
         'descrizione': "I am out of town this weekend and my pet sitter is sick! I am looking for a last minute help with my two cats. Please, I am desperate!",
         'date': "2022-03-19", 'lat': "45.031349418202346", 'lng': "7.650670868351874",
         'placeId': "ChIJk67CatsSiEcRwIxAtahQVQg", 'address': "Via Nizza 129"},
        {'titolo': "Moving out",
         'descrizione': "Hello! I am moving out of my house and all of my friends are busy. I am looking for someone that can help me. I have a lot of books and they may be heavy. Thank you!",
         'date': "2022-02-24", 'lat': "45.06489699683761", 'lng': "7.630211069168476",
         'placeId': "ChIJu6nBNJVsiEcRjUReMrrGsg0", 'address': "Via Monginevro 3"},
        {'titolo': "After-school activities",
         'descrizione': "I am looking for someone who can help my children of 12 years old with some math exercises.",
         'date': "2022-03-28", 'lat': "45.07150270339428", 'lng': "7.6755482647576425",
         'placeId': "ChIJbQiBvnJtiEcRuxTkED8C4I8", 'address': "Via Cernaia 8"},
        {'titolo': "Looking for a gardening expert",
         'descrizione': "I am looking for someone who has a passion in gardening that can help me with my plants.",
         'date': "2022-06-28", 'lat': "45.062928866175696", 'lng': "7.701314035921153",
         'placeId': "ChIJ-f-CvJ5yiEcR9YkHqilhGP8", 'address': "Via Umberto Cosmo 6"}
    ]

    ids = {5, 6, 7, 5, 6, 7, 5}

    for studente in studenti:
        mail = studente['name'].lower() + studente['surname'].lower() + '@mail.com'
        user_db = Student(first_name=studente['name'],
                          surname=studente['surname'],
                          email=mail,
                          description=studente['description'],
                          password=generate_password_hash('1234567890', method='sha256'),
                          type='student')
        db.session.add(user_db)
        db.session.commit()

    for adulto in adulti:
        mail = adulto['name'].lower() + adulto['surname'].lower() + '@mail.com'
        user_db = Adult(first_name=adulto['name'],
                        surname=adulto['surname'],
                        email=mail,
                        description=adulto['description'],
                        password=generate_password_hash('1234567890', method='sha256'),
                        type='adult')
        db.session.add(user_db)
        db.session.commit()

    for task in tasks:
        b = 5
        dt = datetime.strptime(task['date'], '%Y-%m-%d')
        de = dt - timedelta(days=4)
        us = User.query.get(b)
        b += 1

        new_offer = Offer(title=task['titolo'], description=task['descrizione'], date_task=dt, amount=10, dateexpire=de,
                          id_adult=us.id, lat=task['lat'], lng=task['lng'], placeId=task['placeId'],
                          address=task['address'])
        db.session.add(new_offer)
        db.session.commit()

    applicant = User.query.get(1)
    offer1 = Offer.query.get(1)
    offer1.applicants.append(applicant)
    applicant2 = User.query.get(2)
    offer1.applicants.append(applicant2)
    print offer1.applicants
    db.session.commit()
