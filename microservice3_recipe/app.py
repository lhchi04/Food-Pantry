import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mock data for available items in the food pantry
available_items = [
    {"id": 1, "name": "Apple"},
    {"id": 2, "name": "Banana"},
    {"id": 3, "name": "Flour"},
    {"id": 4, "name": "Sugar"},
    {"id": 5, "name": "Milk"}
]

# Endpoint to list available items in the food pantry
@app.route('/pantry/items', methods=['GET'])
def list_items():
    return jsonify(available_items)

# Endpoint to allow clients to select items from the food pantry by specifying IDs
selected_items = []

@app.route('/pantry/select', methods=['POST'])
def select_items_by_ids():
    if request.method == 'POST':
        data = request.get_json()
        selected_ids = data.get('selected_ids', [])

        # Clear the previous selection and update with the new one
        selected_items.clear()
        for item_id in selected_ids:
            item = next((item for item in available_items if item['id'] == item_id), None)
            if item:
                selected_items.append(item)

        # Return a success message
        return jsonify({'message': 'Items selected successfully', 'selected_items': selected_items})
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

# Endpoint to generate recipes based on selected items
@app.route('/pantry/recipes', methods=['GET'])
def generate_recipes():
    # Call Recipe Microservice to generate recipes based on selected items
    recipe_response = requests.get('http://localhost:5001/recipes', params={'items': [item['name'] for item in selected_items]})
    if recipe_response.status_code == 200:
        recipes = recipe_response.json()
        return jsonify(recipes)
    else:
        return jsonify({'error': 'Failed to generate recipes'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
