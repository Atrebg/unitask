from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Review(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    id_reviewer = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_reviewed = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('offer.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    type = db.Column(db.String(20))
    recensionipostate = db.relationship('Review', foreign_keys='Review.id_reviewer',
                                        backref='author')
    recensioniricevute = db.relationship('Review', foreign_keys='Review.id_reviewed',
                                         backref='ricevitore')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user',
    }


application_table = db.Table('application_table',
                             db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                             db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'))
                             )


class Student(User, db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    position = db.Column(db.String(150))
    applications = db.relationship('Offer', secondary=application_table, backref='applicants')
    performed = db.relationship('Offer', backref='performer')

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


class Adult(User, db.Model):
    __tablename__ = 'adult'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tasks = db.relationship('Offer')

    __mapper_args__ = {
        'polymorphic_identity': 'adult',
    }


class Offer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    isAss = db.Column(db.Boolean, default=False)
    date_task = db.Column(db.DateTime(timezone=True))
    id_adult = db.Column(db.Integer, db.ForeignKey('adult.id'))
    scelta = db.Column(db.Integer, db.ForeignKey('student.id'))
    isPerf = db.Column(db.Boolean, default=False)
    rece = db.relationship('Review', backref='recensione', uselist=False)


    #applications = db.relationship("Student", secondary=application_table)
    #db.UniqueConstraint('applications')
    # id_student = db.Column(db.Integer, db.ForeignKey('user.id'))
