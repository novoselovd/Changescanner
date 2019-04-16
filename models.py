from flask_login import UserMixin
from app import db
from pytz import timezone
from datetime import datetime

UTC = timezone('UTC')


def time_now():
    return str(datetime.now(timezone('Europe/Moscow')).strftime('%B %dth, %Y'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email_confirmed = db.Column(db.Boolean(), default=0)
    coms = db.relationship('Comment', backref='User', lazy='dynamic')
    subscriptions = db.relationship('Subscriptions', backref='User', lazy='dynamic')


class Exchangers(db.Model):
    __bind_key__ = 'exchangers'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(50))
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    country = db.Column(db.String)
    comments = db.Column(db.Integer, default=0)
    positives = db.Column(db.Integer, default=0)
    complains = db.Column(db.Integer, default=0)
    image = db.Column(db.String)
    XMLlink = db.Column(db.String(50))
    dateOfCreation = db.Column(db.String(50))
    badges = db.Column(db.String(500))
    ownerId = db.Column(db.Integer, default=0)
    coms = db.relationship('Comment', backref='Exchanger', lazy='dynamic')
    rates = db.relationship('Rates', backref='Exchanger', lazy='dynamic')


class Comment(UserMixin, db.Model):
    __bind_key__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(200))
    commentTime = db.Column(db.String, default=time_now())
    type = db.Column(db.String(50))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    userName = db.Column(db.String(50))
    byAdmin = db.Column(db.Integer, default=0)
    exchangerId = db.Column(db.Integer, db.ForeignKey('exchangers.id'))


class Rates(UserMixin, db.Model):
    __bind_key__ = 'rates'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))
    give = db.Column(db.Float)
    get = db.Column(db.Float)
    coef = db.Column(db.Float)
    exchangerId = db.Column(db.Integer, db.ForeignKey('exchangers.id'))


class Subscriptions(UserMixin, db.Model):
    __bind_key__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))
    coef = db.Column(db.Float)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))



