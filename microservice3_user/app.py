from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Placeholder for user storage, replace with database integration
users = {}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({'error': 'User already exists'}), 409
    
    hashed_password = generate_password_hash(password)
    users[username] = {'password': hashed_password}
    
    return jsonify({'message': 'User registered successfully', 'user_id': username}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful', 'user_id': username}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile/<username>', methods=['GET', 'PUT'])
# def profile(username):
#     user = users.get(username)
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
#     if request.method == 'GET':
#         user = users.get(username)
#         if not user:
#             return jsonify({'error': 'User not found'}), 404
#         return jsonify({'username': username, 'profile': user})
#     else:
#         # data = request.get_json()
#         # if 'password' in data:
#         #     users[username]['password'] = generate_password_hash(data['password'])
#         # return jsonify({'message': 'Profile updated successfully'}), 200

#         data = request.get_json()
#         current_password = data.get('current_password')
#         new_password = data.get('new_password')

#         user = users.get(username)
#         if user and 'password' in data and check_password_hash(user['password'], current_password):
#             users[username]['password'] = generate_password_hash(new_password)
#             return jsonify({'message': 'Profile updated successfully'}), 200
#         else:
#             return jsonify({'error': 'Invalid current password'}), 401
def profile(username):
    user = users.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({'username': username, 'profile': user})

    elif request.method == 'PUT':
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if current_password and new_password and check_password_hash(user['password'], current_password):
            users[username]['password'] = generate_password_hash(new_password)
            return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Invalid current password'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5002)
