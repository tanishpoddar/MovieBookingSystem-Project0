from flask import Blueprint, request, jsonify
from app.controllers import food_controller

bp = Blueprint('food_routes', __name__)

@bp.route('/order', methods=['POST'])
def order_food():
    data = request.json
    response = food_controller.order_food(data)
    return jsonify(response)
