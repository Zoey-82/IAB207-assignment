from . import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(50), nullable=False)
    street_address = db.Column(db.String(250), nullable=False)
    events = db.relationship('Event', backref='owner', lazy=True)
    bookings = db.relationship('Order', backref='customer', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Open')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='event', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='orders')
    event = db.relationship('Event', backref='orders')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
