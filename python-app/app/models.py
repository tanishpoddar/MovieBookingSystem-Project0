from app.extensions import db
from datetime import datetime

class Theater(db.Model):
    __tablename__ = 'theater'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    screens = db.relationship('Screen', backref='theater', lazy=True)

class Screen(db.Model):
    __tablename__ = 'screen'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Gold, Max, General
    price = db.Column(db.Float, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))
    show_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    bookings = db.relationship('Booking', backref='screen', lazy=True)
    waiting_list = db.relationship('WaitingList', backref='screen', lazy=True)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seats_booked = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    food_items = db.relationship('FoodOrder', backref='booking', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled

class WaitingList(db.Model):
    __tablename__ = 'waiting_list'
    id = db.Column(db.Integer, primary_key=True)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seats_required = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), default='waiting')  # waiting, allocated, expired

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    waiting_list = db.relationship('WaitingList', backref='user', lazy=True)

class FoodBeverage(db.Model):
    __tablename__ = 'food_beverage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class FoodOrder(db.Model):
    __tablename__ = 'food_order'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food_beverage.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)