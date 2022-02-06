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
    description = db.Column(db.String(150))
    type = db.Column(db.String(20))
    reviewsposted = db.relationship('Review', foreign_keys='Review.id_reviewer',
                                    backref='author')
    reviewsreceived = db.relationship('Review', foreign_keys='Review.id_reviewed',
                                      backref='received')

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

    def controlapplication(self, task):
        if task in self.applications:
            return False
        return True

    def taskwon(self):
        ltaskwon = []
        for off in self.applications:
            if off.scelta == self.id:
                ltaskwon.append(off)
        return ltaskwon

    def taskwonandperform(self):
        t = []
        for off in self.applications:
            if off.scelta == self.id and off.isPerf:
                t.append(off)
        return t

    def tasklost(self):
        t = []
        for off in self.applications:
            if off.scelta != self.id and off.scelta:
                t.append(off)
        return t

    def getapplications(self):
        t=self.applications
        return t


class Adult(User, db.Model):
    __tablename__ = 'adult'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tasks = db.relationship('Offer', backref='poster')

    __mapper_args__ = {
        'polymorphic_identity': 'adult',
    }


class Offer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(150))
    address = db.Column(db.String(150))
    placeId = db.Column(db.String(150))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    isAss = db.Column(db.Boolean, default=False)
    date_task = db.Column(db.DateTime(timezone=True))
    id_adult = db.Column(db.Integer, db.ForeignKey('adult.id'))
    scelta = db.Column(db.Integer, db.ForeignKey('student.id'))
    isPerf = db.Column(db.Boolean, default=False)
    rece = db.relationship('Review', backref='recensione')
    isClosed = db.Column(db.Boolean, default=False)

    # applications = db.relationship("Student", secondary=application_table)
    # db.UniqueConstraint('applications')
    # id_student = db.Column(db.Integer, db.ForeignKey('user.id'))
    @staticmethod
    def controltasksdate():
        from datetime import datetime
        today = datetime.today()
        for task in Offer.query.filter(Offer.isClosed == False):
            if task.date_task <= today and task.isAss == False:
                task.isClosed = True

        db.session.commit()

    def controldate(self):
        from datetime import datetime
        today = datetime.today()
        if self.date_task <= today:
            self.isClosed = True
            db.session.commit()
            return False
        return True

    def __contains__(self, user):
        for a in self.applicants:
            if a.id == user.id:
                return True
        return False

    def getdict(self):
        a = {"title": self.title, "address1": self.address, "address2": "Torino",
             "coords": {"lat": self.lat, "lng": self.lng},
             "placeId": self.placeId, "task_id": self.id}

        return a

# {"title": "Death Valley National Park", "address1": "California", "address2": "United States",
#    "coords": {"lat": 36.4617, "lng": -116.8668}, "placeId": "ChIJR4qudndLx4ARVLDye3zwycw"},
