from flask import Blueprint, jsonify, render_template, request
from app.models import Theater, Screen, User, FoodBeverage, Booking, WaitingList
from datetime import datetime

bp = Blueprint('theater', __name__)

@bp.route('/')
def index():
    theaters = Theater.query.all()
    food_items = FoodBeverage.query.all()
    user = User.query.first()  # For demo purposes
    return render_template('home.html', 
                         theaters=theaters, 
                         food_items=food_items,
                         user=user)

@bp.route('/<int:theater_id>/screens')
def get_screens(theater_id):
    screens = Screen.query.filter_by(theater_id=theater_id).all()
    return jsonify([{
        'id': screen.id,
        'type': screen.type,
        'price': screen.price,
        'seats_available': screen.seats_available,
        'show_time': screen.show_time.strftime('%Y-%m-%d %H:%M')
    } for screen in screens])

@bp.route('/my-bookings')  # Changed route name
def view_bookings():
    user = User.query.first()  # For demo purposes
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.created_at.desc()).all()
    return render_template('bookings.html', bookings=bookings, datetime=datetime)

@bp.route('/my-waitlist')  # Changed route name
def view_waiting_list():
    user = User.query.first()  # For demo purposes
    waiting_list = WaitingList.query.filter_by(
        user_id=user.id,
        status='waiting'
    ).order_by(WaitingList.created_at.desc()).all()
    return render_template('waiting_list.html', waiting_list=waiting_list)