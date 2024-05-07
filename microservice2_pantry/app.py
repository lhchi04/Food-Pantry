from flask import Flask, redirect, request, jsonify, url_for

app = Flask(__name__)

pantry_items = [
    {'ID': 1, 'Name': 'Pasta', 'Quantity': 2},
    {'ID': 2, 'Name': 'Rice', 'Quantity': 50},
    {'ID': 3, 'Name': 'Tomato', 'Quantity': 50},
    {'ID': 4, 'Name': 'Ham', 'Quantity': 50},
    {'ID': 5, 'Name': 'Butter', 'Quantity': 50},
    {'ID': 6, 'Name': 'Apple', 'Quantity': 50},
    {'ID': 7, 'Name': 'Banana', 'Quantity': 1},
    {'ID': 8, 'Name': 'Spam', 'Quantity': 50},
    {'ID': 9, 'Name': 'Egg', 'Quantity': 50},
    {'ID': 10, 'Name': 'Corn', 'Quantity': 50},
    {'ID': 11, 'Name': 'Milk', 'Quantity': 50},
    {'ID': 12, 'Name': 'Coffee', 'Quantity': 50},
    {'ID': 13, 'Name': 'Noodles', 'Quantity': 50},
    {'ID': 14, 'Name': 'Sausage', 'Quantity': 50},
    {'ID': 15, 'Name': 'Chocolate', 'Quantity': 50},
]

@app.route('/pantry_items')
def home():
    # Filtering items to only include those with quantity > 0
    items_data = [item for item in pantry_items if item['Quantity'] > 0]
    return jsonify(items_data)

# Initialize a global dictionary to store cart contents
global_cart_contents = {}

@app.route('/add_items_to_cart', methods=['POST'])
def add_items_to_cart():
    selected_items = request.form.getlist('items')
    for item_id_str in selected_items:
        item_id = int(item_id_str)
        item = next((item for item in pantry_items if item['ID'] == item_id), None)
        if item and item['Quantity'] > 0:  # Check if item exists and is in stock
            if item_id not in global_cart_contents:
                global_cart_contents[item_id] = 0
            global_cart_contents[item_id] += 1
            item['Quantity'] -= 1  # Decrement stock
    return redirect(url_for('view_cart'))

@app.route('/view_cart')
def view_cart():
    cart_items = {}
    for item_id, qty in global_cart_contents.items():
        item = next((item for item in pantry_items if item['ID'] == item_id), None)
        if item:
            cart_items[item['Name']] = qty
    return jsonify(cart_items)

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    data = request.get_json()
    item_name = data['item_name']
    quantity = int(data['quantity'])  # Quantity to be added back to the stock

    item = next((item for item in pantry_items if item['Name'] == item_name), None)
    if item is None:
        return jsonify({'error': f'Item "{item_name}" not found in the pantry.'}), 404

    item['Quantity'] += quantity
    if item['ID'] in global_cart_contents:
        if global_cart_contents[item['ID']] > quantity:
            global_cart_contents[item['ID']] -= quantity
        else:
            global_cart_contents.pop(item['ID'])
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)