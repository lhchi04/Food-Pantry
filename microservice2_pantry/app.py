from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PantryItem(db.Model):
    __tablename__ = 'PantryItems'  # Ensure this exactly matches the table name in the database
    ID = db.Column(db.Integer, primary_key=True)  # Capital 'ID' to match your schema description
    Name = db.Column(db.String(50), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'ID': self.ID,
            'Name': self.Name,
            'Quantity': self.Quantity
        }

@app.route('/pantry_items')
def home():
    items = PantryItem.query.all()  # Retrieve all items from the PantryItems table
    items_data = [item.to_dict() for item in items]  # Convert each item to a dictionary
    return jsonify(items_data)

# Initialize a global dictionary to store cart contents
global_cart_contents = {}

@app.route('/add_items_to_cart', methods=['POST'])
def add_items_to_cart():
    selected_items = request.form.getlist('items')
    for item_id_str in selected_items:
        item_id = int(item_id_str)
        item = PantryItem.query.get(item_id)
        if item and item.Quantity > 0:  # Check if item exists and is in stock
            if item_id not in global_cart_contents:
                global_cart_contents[item_id] = 0
            global_cart_contents[item_id] += 1
            item.Quantity -= 1  # Decrement stock
            db.session.commit()  # Save changes to the database
    return redirect(url_for('view_cart'))

@app.route('/view_cart')
def view_cart():
    # items = PantryItem.query.filter(PantryItem.ID.in_(global_cart_contents.keys())).all()
    # cart_items = {item.Name: global_cart_contents[item.ID] for item in items if item}
    cart_items = {PantryItem.query.get(item_id).Name: qty for item_id, qty in global_cart_contents.items() if PantryItem.query.get(item_id)}
    return jsonify(cart_items)

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    data = request.get_json()
    item_name = data['item_name']
    quantity = int(data['quantity'])  # Quantity to be added back to the stock

    # Query the database for the PantryItem
    item = PantryItem.query.filter_by(Name=item_name).first()
    
    if item is None:
        return jsonify({'error': f'Item "{item_name}" not found in the pantry.'}), 404
    # Add back the quantity to the item in the database
    item.Quantity += quantity
    db.session.commit()

    # Remove the item from the global cart
    global_cart_contents.pop(item.ID)
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
