from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for user profiles (replace with a database in production)
user_profiles = {}


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    name = data['name']
    email = data['email']
    
    if email in user_profiles:
        return jsonify({'error': 'Email already exists'}), 409
    
    user_profiles[email] = {'name': name, 'email': email}
    return jsonify({'message': 'User profile created successfully'}), 201


@app.route('/users/<string:email>', methods=['GET'])
def get_user(email):
    if email not in user_profiles:
        return jsonify({'error': 'User profile not found'}), 404
    
    return jsonify(user_profiles[email])


if __name__ == '__main__':
    app.run(debug=True)
