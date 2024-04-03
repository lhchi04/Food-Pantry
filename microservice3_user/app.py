import os
import json
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
import time

app = Flask(__name__)
api = Api(app)

users = dict()
taken_usernames = set()

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
        return jsonify({'session': hex(hash(name + "secret" + str(current_time)))}), 200

if __name__ == '__main__':
    app.run(debug=True)