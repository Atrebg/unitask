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
    pass


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    type = db.Column(db.String(20))
    reviewedmade = db.relationship('Review', foreign_keys=[Review.id_reviewed],)
    reviewsubite = db.relationship('Review', foreign_keys=[Review.id_reviewer],)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }


application_table = db.Table('application_table',
                             db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                             db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'))
                             )


class Student(User):
    __tablename__ = 'student'
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    applications = db.relationship('Offer', secondary=application_table, backref=db.backref('applicant'))


class Adult(User):
    __tablename__ = 'adult'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tasks = db.relationship('Offer', back_populates="adult")

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
    adult = db.relationship("Adult", back_populates="tasks")
    scelta = db.Column(db.Integer)

    # applications = db.relationship("Student", secondary=application_table)
    # id_student = db.Column(db.Integer, db.ForeignKey('user.id'))