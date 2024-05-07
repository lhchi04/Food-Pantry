
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Placeholder for user storage, structured dictionary with user ID
users = {}
user_id_counter = 1

@app.route('/signup', methods=['POST'])
def signup():
    global user_id_counter
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({'error': 'User already exists'}), 409
    
    hashed_password = generate_password_hash(password)
    users[username] = {'id': user_id_counter, 'password': hashed_password}
    user_id = user_id_counter
    user_id_counter += 1
    
    return jsonify({'message': 'User registered successfully', 'user_id': user_id, 'username': username}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful', 'user_id': user['id'], 'username': username}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    user = users.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({'username': username, 'user_id': user['id']})

    elif request.method == 'POST':
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if current_password and new_password and check_password_hash(user['password'], current_password):
            users[username]['password'] = generate_password_hash(new_password)
            return jsonify({'message': 'Profile updated successfully', 'user_id': user['id']}), 200
        else:
            return jsonify({'error': 'Invalid current password'}), 401
        
@app.route('/status')
def status():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
