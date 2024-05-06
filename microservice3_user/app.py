from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'  # Set a secret key for session management

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        """
        Return a dictionary containing the user data.
        """
        return {
            'id': self.id,
            'username': self.username,
        }

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        print("Session Username:", session.get('username'))
        print("Session User ID:", session.get('user_id'))
        return jsonify({'message': 'Login successful', 'user_id': user.id, 'username': user.username}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    # if 'username' not in session:
    #     return jsonify({'error': 'Unauthorized access'}), 401
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({'username': user.username})

    elif request.method == 'POST':
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Check for the presence of required data
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password must be provided'}), 400

        # Verify the current password before updating
        if check_password_hash(user.password_hash, current_password):
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Invalid current password'}), 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('status'))

@app.route('/status')
def status():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)

