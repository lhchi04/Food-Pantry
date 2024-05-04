from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

pantry_items = {
    1: {'name': 'Pasta', 'quantity': 50},
    2: {'name': 'Tomato Sauce', 'quantity': 30},
    3: {'name': 'Beans', 'quantity': 20},
    4: {'name': 'Rice', 'quantity': 40},
    5: {'name': 'Tuna', 'quantity': 25}
}

@app.route('/pantry_items', methods=['GET'])
def get_pantry_items():
    return jsonify(pantry_items)

@app.route('/add_items_to_cart', methods=['POST'])
def add_items_to_cart():
    selected_items = request.json.get('items', [])
    cart_items = {}

    for item_id in selected_items:
        item_id = int(item_id)
        if item_id in pantry_items and pantry_items[item_id]['quantity'] > 0:
            cart_items[item_id] = pantry_items[item_id]
            pantry_items[item_id]['quantity'] -= 1  # Reduce inventory

    return jsonify(cart_items)

if __name__ == '__main__':
    app.run(debug=True, port=5003)