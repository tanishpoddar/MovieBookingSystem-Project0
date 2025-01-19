from app.models import Theater, Screen, FoodBeverage, User
from app.extensions import db
from datetime import datetime, timedelta

def init_db():
    db.drop_all()
    db.create_all()

    # Create test user
    user = User(username="testuser", email="test@example.com")
    db.session.add(user)

    # Create theaters
    theaters = [
        Theater(name="PVR Cinemas"),
        Theater(name="INOX Movies")
    ]
    
    for theater in theaters:
        db.session.add(theater)
    db.session.commit()

    # Create screens for each theater
    screen_configs = [
        {"type": "Gold", "price": 400, "seats": 2},
        {"type": "Max", "price": 300, "seats": 5},
        {"type": "General", "price": 200, "seats": 10}
    ]

    # Add screens to each theater
    for theater in theaters:
        for i, config in enumerate(screen_configs, 1):
            screen = Screen(
                number=i,
                type=config["type"],
                price=config["price"],
                seats_available=config["seats"],
                theater_id=theater.id,
                show_time=datetime.now() + timedelta(hours=2)  # Show time 2 hours from now
            )
            db.session.add(screen)

    # Add food items
    food_items = [
        {"name": "Popcorn", "price": 150},
        {"name": "Sandwich", "price": 120}
    ]
    
    for item in food_items:
        food = FoodBeverage(name=item["name"], price=item["price"])
        db.session.add(food)

    db.session.commit()