from app.models import FoodBeverage


def get_all_food_items():
    food_items = FoodBeverage.query.all()
    return [{'id': food.id, 'name': food.name, 'price': food.price} for food in food_items]
# Add this to food_controller.py
def order_food(data):
    try:
        food_items = FoodBeverage.query.filter(FoodBeverage.id.in_([item['id'] for item in data['items']])).all()
        total_price = sum(item.price for item in food_items)
        return {"message": "Order placed successfully", "total": total_price}
    except Exception as e:
        return {"error": str(e)}, 400