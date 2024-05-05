import os
import requests
from flask import Flask, request, jsonify, redirect, render_template, session, url_for, flash
from flask_restful import Api

# Configuration
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5002')
PANTRY_SERVICE_URL = os.getenv('PANTRY_SERVICE_URL', 'http://localhost:5003')
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
            return render_template('login.html', error='Incorrect username or password.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = requests.post(f'{USER_SERVICE_URL}/signup', json=request.form.to_dict())
        if response.status_code == 201:
            session['user_id'] = response.json()['user_id']
            return redirect(url_for('pantry'))
        else:
            return render_template('signup.html', error='Username already exists')
    return render_template('signup.html')

@app.route('/user_profile/<username>', methods=['GET', 'POST'])
def user_profile(username):
    if 'user_id' not in session or session['user_id'] != username:
        return redirect(url_for('login'))
    if request.method == 'GET':
        response = requests.get(f'{USER_SERVICE_URL}/profile/{username}')
        if response.status_code == 200:
            profile_info = response.json()
            return render_template('profile.html', profile=profile_info)
        else:
            return "Error loading profile", response.status_code
    else:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if not current_password or not new_password:
            return render_template('profile.html', error_message="Both current and new passwords are required")

        response = requests.put(
            f'{USER_SERVICE_URL}/profile/{username}',
            json={
                'current_password': current_password,
                'new_password': new_password
            }
        )
        if response.status_code == 200:
            flash('Your password has been updated successfully!', 'success')
            return redirect(url_for('user_profile', username=username))
        else:
            flash('Failed to update password. Please check your current password and try again.', 'error')
            return redirect(url_for('user_profile', username=username))

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
        
@app.route('/recipe', methods=['GET'])
def recipe():
    response = requests.get(f'{RECIPE_SERVICE_URL}/status')
    return "Running", response.status_code

@app.route('/health')
def health_check():
    # Add your custom health check logic here
    if all_required_services_are_running():
        return 'OK', 200
    else:
        return 'Service Unavailable', 500
def all_required_services_are_running():
    # try:
    #     # Attempt to reach the status endpoint of the user microservice
    #     response = requests.get(f"{USER_SERVICE_URL}/status", timeout=5)
    #     if response.status_code == 200:
    #         return True
    #     else:
    #         return False
    # except requests.RequestException as e:
    #     return jsonify({'status': 'ERROR', 'message': f'Failed to reach user service: {str(e)}'}), 503
    return True

if __name__ == '__main__':
    app.run(debug=True, port=5000)