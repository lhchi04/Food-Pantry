from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for the shopping cart (replace with a database in production)
shopping_cart = {}

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    if 'item' not in data or 'quantity' not in data:
        return jsonify({'error': 'Item and quantity are required'}), 400

    item = data['item']
    quantity = data['quantity']

    if item not in shopping_cart:
        shopping_cart[item] = quantity
    else:
        shopping_cart[item] += quantity

    return jsonify({'message': 'Item added to cart successfully'}), 201

@app.route('/cart', methods=['GET'])
def view_cart():
    return jsonify(shopping_cart)

if __name__ == '__main__':
    app.run(debug=True)
