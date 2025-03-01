from flask import Blueprint, request, jsonify, flash, redirect, url_for
from app.controllers import booking_controller
from app.models import User, WaitingList
from app import db

bp = Blueprint('booking', __name__)

@bp.route('/book', methods=['POST'])
def book_ticket():
    try:
        data = {
            'screen_id': request.form.get('screen_id'),
            'seats': request.form.get('seats'),
            'food_items[]': request.form.getlist('food_items[]')
        }
        
        if not data['screen_id'] or not data['seats']:
            flash('Please select screen and seats', 'error')
            return redirect(url_for('theater.index'))
            
        response, status_code = booking_controller.book_ticket(data)
        flash(response.get('message', 'Booking failed!'), 'success' if status_code == 200 else 'error')
        return redirect(url_for('theater.index'))
        
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('theater.index'))

@bp.route('/waitlist/add', methods=['POST'])
def add_to_waitlist():
    try:
        screen_id = request.form.get('screen_id')
        seats = int(request.form.get('seats', 1))
        user = User.query.first()

        waiting = WaitingList(
            screen_id=screen_id,
            user_id=user.id,
            seats_required=seats,
            status='waiting'
        )
        db.session.add(waiting)
        db.session.commit()

        flash('Added to waiting list successfully!', 'success')
        return redirect(url_for('theater.index'))
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('theater.index'))

@bp.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    try:
        response, status_code = booking_controller.cancel_booking(booking_id)
        flash(response.get('message', 'Cancellation failed!'), 'success' if status_code == 200 else 'error')
        return redirect(url_for('theater.index'))
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('theater.index'))