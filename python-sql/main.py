from datetime import datetime, timedelta
from database import Session, Theater, Screen, ScreenType, FoodOrder, WaitingList, Booking
from booking_system import BookingSystem

def initialize_sample_data():
    session = Session()
    session.query(FoodOrder).delete()
    session.query(WaitingList).delete()
    session.query(Booking).delete()
    session.query(Screen).delete()
    session.query(Theater).delete()
    theaters = [
        Theater(name="PVR Cinemas", location="Delhi"),
        Theater(name="INOX", location="Delhi")
    ]
    session.add_all(theaters)
    session.commit()
    for theater in theaters:
        screens = [
            Screen(theater_id=theater.id, screen_type=ScreenType.GOLD, 
                   total_seats=2, movie_name="Inception", 
                   show_time=datetime.now() + timedelta(hours=2)),
            Screen(theater_id=theater.id, screen_type=ScreenType.MAX, 
                   total_seats=5, movie_name="Avatar", 
                   show_time=datetime.now() + timedelta(hours=3)),
            Screen(theater_id=theater.id, screen_type=ScreenType.GENERAL, 
                   total_seats=10, movie_name="Iron Man", 
                   show_time=datetime.now() + timedelta(hours=1))
        ]
        session.add_all(screens)
    session.commit()

def display_menu():
    print("\n=== Movie Booking System ===")
    print("1. Book Ticket")
    print("2. Cancel Ticket")
    print("3. Exit")
    return input("Select option: ")

def book_ticket(booking_system):
    theaters = booking_system.session.query(Theater).all()
    print("\nSelect Theater:")
    for i, theater in enumerate(theaters, 1):
        print(f"{i}. {theater.name}")
    theater_choice = int(input("Enter theater number: "))
    theater = theaters[theater_choice-1]
    print("\nSelect Screen Type:")
    print("1. Gold (Rs. 400)")
    print("2. IMAX (Rs. 300)")
    print("3. General (Rs. 200)")
    screen_choice = int(input("Enter screen type: "))
    screen_types = [ScreenType.GOLD, ScreenType.MAX, ScreenType.GENERAL]
    screen_type = screen_types[screen_choice-1]
    ticket_price = booking_system.screen_prices[screen_type]
    name = input("\nEnter your name: ")
    food_total = 0
    food_items = {}
    if input("\nWant to add food? (y/n): ").lower() == 'y':
        print("\nEnter quantity (0 if none):")
        popcorn_qty = int(input("Popcorn (Rs. 150): "))
        sandwich_qty = int(input("Sandwich (Rs. 100): "))
        if popcorn_qty > 0:
            food_items['popcorn'] = popcorn_qty
            food_total += 150 * popcorn_qty
        if sandwich_qty > 0:
            food_items['sandwich'] = sandwich_qty
            food_total += 100 * sandwich_qty
        if screen_type == ScreenType.GOLD:
            food_total *= 0.9  # 10% discount
            print("\nApplied 10% food discount (Gold)")
        elif screen_type == ScreenType.MAX:
            food_total *= 0.95  # 5% discount
            print("\nApplied 5% food discount (IMAX)")
    print("\nPrice Breakdown:")
    print(f"Ticket Price: Rs. {ticket_price}")
    if food_total > 0:
        print(f"Food Total: Rs. {food_total:.2f}")
    print(f"Total Amount: Rs. {ticket_price + food_total:.2f}")
    if input("\nConfirm booking? (y/n): ").lower() == 'y':
        result, booking_id = booking_system.book_ticket(
            theater_id=theater.id,
            screen_type=screen_type,
            user_name=name,
            food_items=food_items
        )
        print(f"\nResult: {result}")
        print(f"Your Booking ID: {booking_id}")

def cancel_ticket(booking_system):
    booking_id = int(input("\nEnter booking ID to cancel: "))
    result = booking_system.cancel_ticket(booking_id)
    print(f"\nResult: {result}")

def test_waiting_list():
    booking_system = BookingSystem()
    theater = booking_system.session.query(Theater).first()
    for i in range(3):
        result = booking_system.book_ticket(
            theater_id=theater.id,
            screen_type=ScreenType.GOLD,
            user_name=f"User{i}"
        )
        print(f"Booking {i+1} result:", result)
    result = booking_system.book_ticket(
        theater_id=theater.id,
        screen_type=ScreenType.GOLD,
        user_name="WaitingUser"
    )
    print("\nWaiting list booking result:", result)
    booking = booking_system.session.query(Booking).first()
    result = booking_system.cancel_ticket(booking.id)
    print("\nCancellation result:", result)

def main():
    initialize_sample_data()
    booking_system = BookingSystem()
    while True:
        choice = display_menu()
        if choice == '1':
            book_ticket(booking_system)
        elif choice == '2':
            cancel_ticket(booking_system)
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()