import os
import json
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
import time

app = Flask(__name__)
api = Api(app)

# Dummy data
items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1", "price": 10.99},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2", "price": 19.99},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3", "price": 14.99}
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404

# Swagger UI configuration
# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'

# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "User Authentication API"
#     }
# )
# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)