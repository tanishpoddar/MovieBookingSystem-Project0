from app.controllers import theater_controller, food_controller
from app.models import Screen, Theater

def get_all_theaters():
    return Theater.query.all()

def get_screens_by_theater(theater_id):
    screens = Screen.query.filter_by(theater_id=theater_id).all()
    return [{'id': screen.id, 'type': screen.type, 'seats_available': screen.seats_available} for screen in screens]
