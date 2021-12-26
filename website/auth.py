# Authentication
import bcrypt as bcrypt
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# We sad clearly that we can accept get and post requests
@auth.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        surname = request.form.get('surName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        tipo=request.form.get('type')

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
            if tipo == 'student':
                new_user = Student(email=email, password=generate_password_hash(password1, method='sha256'), first_name=first_name, surname=surname, type=tipo)
            elif tipo == 'adult':
                new_user = Adult(email=email, password=generate_password_hash(password1, method='sha256'),
                                   first_name=first_name, surname=surname, type=tipo)
            else:
                flash('Type errato scrivere student o adult', category='error')
            db.session.add(new_user)
            riempidb()

            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            if new_user.type == 'student':
                return redirect(url_for('views.offer'))
            
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


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

    for studente in studenti:
        mail = studente['name'].lower() + studente['surname'].lower() + '@mail.com'
        user_db = User(first_name=studente['name'],
                       surname=studente['surname'],
                       email=mail,
                       password_hash=bcrypt.generate_password_hash('1234567890'),
                       type='student')
        db.session.add(user_db)
        db.session.commit()

    for adulto in adulti:
        mail = adulto['name'].lower() + adulto['surname'].lower() + '@mail.com'
        user_db = User(first_name=adulto['name'],
                       surname=adulto['surname'],
                       email=mail,
                       password_hash=bcrypt.generate_password_hash('1234567890'),
                       type='adult')
        db.session.add(user_db)
        db.session.commit()



