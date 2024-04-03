import os
import json
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
import time

app = Flask(__name__)
api = Api(app)

users = dict() # Store usernames and passwords
taken_usernames = set() # Store existed usernames

@app.route('/signup', methods=['POST'])
def sign_up():
    user_info = request.json
    name = user_info['name']
    password = user_info['pwd']
    if name in taken_usernames:
        return jsonify({'error': 'Username is already taken'}), 401
    else:
        current_time = time.time()
        taken_usernames.add(name)
        users[name] = password
        return jsonify({'session': hex(hash(name + "secret" + str(current_time)))}), 200
    
@app.route('/login', methods=['POST'])
def login():
    user_info = request.json
    name = user_info['name']
    password = user_info['pwd']
    if name not in taken_usernames or users[name] != password:
        return jsonify({'error': 'Invalid username or password'}), 401
    else:
        current_time = time.time()
        return jsonify({'session': hex(hash(name + "secret" + str(current_time)))}), 200


if __name__ == '__main__':
    app.run(debug=True)