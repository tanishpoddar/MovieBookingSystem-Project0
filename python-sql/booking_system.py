from datetime import datetime, timedelta
from database import Session, Theater, Screen, Booking, WaitingList, FoodOrder, ScreenType

class BookingSystem:
    def __init__(self):
        self.session = Session()
        self.food_prices = {
            'popcorn': 150,
            'sandwich': 100
        }
        self.screen_prices = {
            ScreenType.GOLD: 400,
            ScreenType.MAX: 300,
            ScreenType.GENERAL: 200
        }
        self.food_discounts = {
            ScreenType.GOLD: 0.10,
            ScreenType.MAX: 0.05,
            ScreenType.GENERAL: 0
        }

    def book_ticket(self, theater_id, screen_type, user_name, food_items=None):
        screen = self.session.query(Screen).filter(
            Screen.theater_id == theater_id,
            Screen.screen_type == screen_type
        ).first()
        if not screen:
            return ("Screen not found", None)
        booked_seats = self.session.query(Booking).filter(
            Booking.screen_id == screen.id,
            Booking.is_cancelled == False
        ).count()
        if booked_seats >= screen.total_seats:
            self._add_to_waiting_list(screen.id, user_name)
            return ("Screen full. Added to waiting list.", None)
        next_seat = booked_seats + 1
        booking = Booking(
            screen_id=screen.id,
            user_name=user_name,
            seat_number=next_seat,
            has_food=bool(food_items)
        )
        self.session.add(booking)
        if food_items:
            discount = self.food_discounts[screen_type]
            for item, quantity in food_items.items():
                price = self.food_prices[item] * quantity * (1 - discount)
                food_order = FoodOrder(
                    booking=booking,
                    item_name=item,
                    quantity=quantity,
                    price=price
                )
                self.session.add(food_order)
        self.session.add(booking)
        self.session.commit()
        return f"Booking successful. Seat number: {next_seat}", booking.id 

    def show_bookings(self):
        bookings = self.session.query(Booking).all()
        print("\nCurrent Bookings:")
        for booking in bookings:
            time_to_show = (booking.screen.show_time - datetime.now()).total_seconds() / 60
            status = "Can cancel" if time_to_show > 30 else "Cannot cancel (< 30 mins to show)"
            print(f"ID: {booking.id} | User: {booking.user_name} | Movie: {booking.screen.movie_name}")
            print(f"Show time: {booking.screen.show_time} | Status: {status}")

    def show_waiting_list(self):
        waiting = self.session.query(WaitingList).all()
        print("\nWaiting List:")
        for entry in waiting:
            time_to_show = (entry.screen.show_time - datetime.now()).total_seconds() / 60
            status = "Active" if time_to_show > 30 else "Expired (< 30 mins to show)"
            print(f"User: {entry.user_name} | Movie: {entry.screen.movie_name} | Status: {status}")
            
    def cancel_ticket(self, booking_id):
        booking = self.session.query(Booking).get(booking_id)
        if not booking:
            return "Booking not found"
        screen = booking.screen
        current_time = datetime.now()
        if current_time + timedelta(minutes=30) > screen.show_time:
            return "Cannot cancel ticket within 30 minutes of show"
        booking.is_cancelled = True
        self.session.commit()
        waiting = self.session.query(WaitingList)\
            .filter(WaitingList.screen_id == screen.id)\
            .order_by(WaitingList.request_time)\
            .first()
        if waiting:
            new_booking = Booking(
                screen_id=screen.id,
                user_name=waiting.user_name,
                seat_number=booking.seat_number
            )
            self.session.add(new_booking)
            self.session.delete(waiting)
            self.session.commit()
            return "Ticket cancelled and allocated to waiting list user"
        return "Ticket cancelled successfully"

    def _add_to_waiting_list(self, screen_id, user_name):
        screen = self.session.query(Screen).get(screen_id)
        if datetime.now() + timedelta(minutes=30) > screen.show_time:
            return "Cannot join waiting list within 30 minutes of show"
        waiting = WaitingList(screen_id=screen_id, user_name=user_name)
        self.session.add(waiting)
        self.session.commit()