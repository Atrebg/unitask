from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    offers = db.relationship('Offer')


class Offer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #date_task = db.Column(db.DateTime(timezone=True))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))


class Review(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    data = db.Column(db.String(150))
    id_poster = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_offer = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_students = db.Column(db.Integer, db.ForeignKey('user.id'))



