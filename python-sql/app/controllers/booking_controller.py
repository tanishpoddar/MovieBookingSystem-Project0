from datetime import datetime, timedelta
from app import db
from app.models import Screen, User, Booking, WaitingList, FoodBeverage
from app.utils.pricing import calculate_food_price, calculate_total_price

def book_ticket(data):
    try:
        screen_id = data.get('screen_id')
        seats = int(data.get('seats', 1))
        food_items = data.get('food_items[]', [])

        # Get screen and validate
        screen = Screen.query.get(screen_id)
        if not screen:
            return {"error": "Invalid screen"}, 400

        # For demo purposes, use first user
        user = User.query.first()
        if not user:
            return {"error": "No user found"}, 400

        available_seats = screen.seats_available

        # Handle partial booking
        if seats > available_seats:
            # Book available seats
            ticket_price = screen.price * available_seats
            remaining_seats = seats - available_seats

            # Add remaining seats to waiting list
            waiting = WaitingList(
                screen_id=screen_id,
                user_id=user.id,
                seats_required=remaining_seats,
                status='waiting'
            )
            db.session.add(waiting)
            db.session.commit()

            # Calculate food price with discount
            food_price = calculate_food_price(food_items, screen.type)

            total_price = ticket_price + food_price

            # Create booking
            booking = Booking(
                screen_id=screen_id,
                user_id=user.id,
                seats_booked=available_seats,
                total_price=total_price,
                status='confirmed',
                created_at=datetime.now()
            )
            db.session.add(booking)

            # Update screen availability
            screen.seats_available -= available_seats
            db.session.commit()

            return {
                "message": f"Booking successful! {available_seats} seats booked, {remaining_seats} seats added to waiting list.",
                "booking_id": booking.id,
                "total_price": total_price,
                "waiting_id": waiting.id
            }, 200

        else:
            # Calculate ticket price
            ticket_price = screen.price * seats

            # Calculate food price with discount
            food_price = calculate_food_price(food_items, screen.type)

            total_price = ticket_price + food_price

            # Create booking
            booking = Booking(
                screen_id=screen_id,
                user_id=user.id,
                seats_booked=seats,
                total_price=total_price,
                status='confirmed',
                created_at=datetime.now()
            )
            db.session.add(booking)

            # Update screen availability
            screen.seats_available -= seats
            db.session.commit()

            return {"message": "Booking successful!", "booking_id": booking.id, "total_price": total_price}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def cancel_booking(booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404

        # Check if cancellation is within allowed time (30 mins before show)
        current_time = datetime.now()
        if current_time + timedelta(minutes=30) >= booking.screen.show_time:
            return {"error": "Cannot cancel less than 30 minutes before show"}, 400

        # Update screen availability
        screen = booking.screen
        screen.seats_available += booking.seats_booked
        
        # Update booking status
        booking.status = 'cancelled'

        # Check waiting list for this screen
        waiting = WaitingList.query.filter_by(
            screen_id=screen.id,
            status='waiting'
        ).order_by(WaitingList.created_at).first()

        if waiting and waiting.seats_required <= screen.seats_available:
            # Create new booking for waiting list user
            new_booking = Booking(
                screen_id=screen.id,
                user_id=waiting.user_id,
                seats_booked=waiting.seats_required,
                total_price=screen.price * waiting.seats_required,
                status='confirmed',
                created_at=datetime.now()
            )
            db.session.add(new_booking)
            
            # Update screen availability
            screen.seats_available -= waiting.seats_required
            
            # Update waiting list status
            waiting.status = 'allocated'

        db.session.commit()
        return {"message": "Booking cancelled successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_waitlist(screen_id):
    try:
        waiting_list = WaitingList.query.filter_by(
            screen_id=screen_id,
            status='waiting'
        ).order_by(WaitingList.created_at).all()
        
        return {
            "waiting_list": [
                {
                    "id": item.id,
                    "user_id": item.user_id,
                    "seats_required": item.seats_required,
                    "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                for item in waiting_list
            ]
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500