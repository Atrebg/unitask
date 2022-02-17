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
         'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi."},
        {'name': "Valeria", 'surname': "Liuni",
         'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi."},
        {'name': "Samuele", 'surname': "Stasi",
         'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi."},
        {'name': "Oliviero", 'surname': "Vidoni",
         'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi."},
    ]

    adulti = [
        {'name': "mamma", 'surname': "papa"},
        {'name': "zia", 'surname': "zio"},
        {'name': "nonno", 'surname': "nonna"},
    ]

    tasks = [
        {'titolo': "cane",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-02-16", 'lat': "45.058427", 'lng': "7.655138", 'placeId': "ChIJbZ33QSFtiEcR3Yr-cxhtfDQ",
         'address': "Corso Lione 40"},
        {'titolo': "gatto",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-02-17", 'lat': "45.07215960121708", 'lng': "7.681296735921444",
         'placeId': "ChIJ-w5Ey3NtiEcRizrB7W-hDNI", 'address': "Via barbaroux 20"},
        {'titolo': "nonna",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-02-18", 'lat': "45.0602789482421", 'lng': "7.659934143334852",
         'placeId': "ChIJx4qR9SJtiEcRqjxf1yPr6KI", 'address': "Via marcopolo 38"},
        {'titolo': "nonno",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-02-19", 'lat': "45.074369423709875", 'lng': "7.6562016089387965",
         'placeId': "ChIJXbcpbQJtiEcRayf8ZeGWbPI", 'address': "Corso Ferrucci 12"},
        {'titolo': "spazzatura",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-02-19", 'lat': "45.031349418202346", 'lng': "7.650670868351874",
         'placeId': "ChIJk67CatsSiEcRwIxAtahQVQg", 'address': "Lingotto"},
        {'titolo': "trasloco",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-02-24", 'lat': "45.06489699683761", 'lng': "7.630211069168476",
         'placeId': "ChIJu6nBNJVsiEcRjUReMrrGsg0", 'address': "Via Monginevro"},
        {'titolo': "compiti",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2022-03-28", 'lat': "45.07150270339428", 'lng': "7.6755482647576425",
         'placeId': "ChIJbQiBvnJtiEcRuxTkED8C4I8", 'address': "Via Cernaia 8"},
        {'titolo': "roba",
         'descrizione': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In consequat nunc non velit posuere, at ultricies est condimentum. Pellentesque sagittis leo euismod nisi mattis condimentum. Etiam vitae eleifend sem. Etiam consectetur vehicula nisl, et consequat massa vestibulum sed. Sed a magna feugiat, rhoncus lacus in, vulputate nisi.",
         'date': "2021-03-28", 'lat': "45.062928866175696", 'lng': "7.701314035921153",
         'placeId': "ChIJ-f-CvJ5yiEcR9YkHqilhGP8", 'address': "Via Umbero cosmo 6"}
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
