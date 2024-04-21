import os
import json
from flask import Flask, request, jsonify
from flask_restful import Api
import requests

app = Flask(__name__)
api = Api(app)

# Mock data for available items in the food pantry
available_items = [
    {"id": 1, "name": "Apple", "description": "shove it in ur ass"},
    {"id": 2, "name": "Banana", "description": "for pads"},
    {"id": 3, "name": "Flour", "description": "ski ski"},
    {"id": 4, "name": "Sugar", "description": "ski twice"},
    {"id": 5, "name": "Milk", "description": "gulp gulp i swallowed all"}
]

# Endpoint to list available items in the food pantry
@app.route('/pantry', methods=['GET'])
def list_items():
    return jsonify(available_items), 200

@app.route('/pantry/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in available_items if item['id'] == item_id), None)
    if item:
        return jsonify(item['description']), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

# @app.route('/pantry/items', methods=['GET'])
# def list_items():
#     """
#     List available items in the food pantry
#     ---
#     responses:
#       200:
#         description: A list of available items
#         content:
#           application/json:
#             schema:
#               type: array
#               items:
#                 $ref: '#/components/schemas/Item'
#     """
#     return jsonify(available_items)

# # Endpoint to allow clients to select items from the food pantry by specifying IDs
# selected_items = []

# @app.route('/pantry/select', methods=['POST'])
# def select_items_by_ids():
#     """
#     Select items from the food pantry by specifying IDs
#     ---
#     parameters:
#       - in: body
#         name: body
#         required: true
#         schema:
#           type: object
#           properties:
#             selected_ids:
#               type: array
#               items:
#                 type: integer
#     responses:
#       200:
#         description: Success message with selected items
#         content:
#           application/json:
#             schema:
#               type: object
#               properties:
#                 message:
#                   type: string
#                 selected_items:
#                   type: array
#                   items:
#                     $ref: '#/components/schemas/Item'
#       405:
#         description: Method Not Allowed
#     """
#     if request.method == 'POST':
#         data = request.get_json()
#         selected_ids = data.get('selected_ids', [])

#         # Clear the previous selection and update with the new one
#         selected_items.clear()
#         for item_id in selected_ids:
#             item = next((item for item in available_items if item['id'] == item_id), None)
#             if item:
#                 selected_items.append(item)

#         # Return a success message
#         return jsonify({'message': 'Items selected successfully', 'selected_items': selected_items})
#     else:
#         return jsonify({"error": "Method Not Allowed"}), 405

# # Endpoint to generate recipes based on selected items
# @app.route('/pantry/recipes', methods=['GET'])
# def generate_recipes():
#     """
#     Generate recipes based on selected items
#     ---
#     responses:
#       200:
#         description: Recipes generated successfully
#         content:
#           application/json:
#             schema:
#               type: array
#               items:
#                 type: string
#       500:
#         description: Failed to generate recipes
#         content:
#           application/json:
#             schema:
#               type: object
#               properties:
#                 error:
#                   type: string
#     """
#     # Ensure that microservice_recipe is running
#     try:
#         response = requests.get('http://localhost:5001/')
#         if response.status_code != 200:
#             return jsonify({'error': 'microservice_recipe is not running or unavailable'}), 500
#     except requests.ConnectionError:
#         return jsonify({'error': 'microservice_recipe is not running or unavailable'}), 500

#     # Call Recipe Microservice to generate recipes based on selected items
#     recipe_response = requests.get('http://localhost:5001/recipes', params={'items': [item['name'] for item in selected_items]})
#     if recipe_response.status_code == 200:
#         recipes = recipe_response.json()
#         return jsonify(recipes)
#     else:
#         return jsonify({'error': 'Failed to generate recipes'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5003)
