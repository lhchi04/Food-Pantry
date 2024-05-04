import os
import requests
from flask import Flask, request, jsonify, redirect, render_template, session, url_for
from flask_restful import Api

# Configuration
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5002')
PANTRY_SERVICE_URL = os.getenv('CATALOGUE_SERVICE_URL', 'http://localhost:5003')
RECIPE_SERVICE_URL = os.getenv('RECIPE_SERVICE_URL', 'http://localhost:5004')

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super_secret_key'  # Should be set to a real secret key in production
api = Api(app)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('pantry'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(f'{USER_SERVICE_URL}/login', json=request.form.to_dict())
        if response.status_code == 200:
            session['user_id'] = response.json()['user_id']
            return redirect(url_for('pantry'))
        else:
            return render_template('login.html', error='Login Failed')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = requests.post(f'{USER_SERVICE_URL}/signup', json=request.form.to_dict())
        if response.status_code == 201:  # Handling the 'Created' status
            session['user_id'] = response.json().get('user_id', None)
            return redirect(url_for('pantry'))
        elif response.status_code == 200:
            session['user_id'] = response.json()['user_id']
            return redirect(url_for('pantry'))
        else:
            return render_template('signup.html', error='Signup Failed')
    return render_template('signup.html')

@app.route('/user_profile/<username>')
def user_profile(username):
    if 'user_id' not in session or session['user_id'] != username:
        return redirect(url_for('login'))
    response = requests.get(f'{USER_SERVICE_URL}/profile/{username}')
    if response.status_code == 200:
        profile_info = response.json()
        return render_template('profile.html', profile=profile_info)
    else:
        return "Error loading profile", response.status_code

@app.route('/update_profile/<username>', methods=['POST'])
def update_profile(username):
    if 'user_id' not in session or session['user_id'] != username:
        return redirect(url_for('login'))
    new_password = request.form.get('password')
    response = requests.put(f'{USER_SERVICE_URL}/profile/{username}', json={'password': new_password})
    if response.status_code == 200:
        return redirect(url_for('user_profile', username=username))
    else:
        return "Error updating profile", response.status_code

@app.route('/logout')
def logout():
    session.clear()  # Clears all data in the session
    return redirect(url_for('login'))

@app.route('/pantry', methods=['GET', 'POST'])
def pantry():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        response = requests.get(f'{PANTRY_SERVICE_URL}/pantry_items')
        if response.status_code == 200:
            items = response.json()
            return render_template('pantry.html', items=items)
        else:
            return jsonify({'error': 'Failed to fetch pantry items'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)


