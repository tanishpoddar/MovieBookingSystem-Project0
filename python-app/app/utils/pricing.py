def calculate_total_price(seats, ticket_price, discount=0):
    subtotal = seats * ticket_price
    return subtotal - (subtotal * discount / 100)

def calculate_food_price(food_items, screen_type):
    discount_rates = {
        "Gold": 10,
        "Max": 5,
        "General": 0
    }

    total_food_cost = sum(item['price'] for item in food_items)
    discount = discount_rates.get(screen_type, 0)
    return total_food_cost - (total_food_cost * discount / 100)