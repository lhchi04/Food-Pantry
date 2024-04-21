import os
import json
import requests
from flask import Flask, request, jsonify, redirect, render_template
from flask_restful import Api
# from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user_info = request.json
    response = requests.post('http://user-svc:80/login', json=user_info)
    if response.status_code == 200:
        # return jsonify({'message': 'Login successful', 'data': response.json()}), 200
        return redirect('/pantry')
    else:
        return jsonify({'error': 'Login failed', 'data': response.json()}), response.status_code

@app.route('/signup', methods=['POST'])
def signup():
    user_info = request.json
    response = requests.post('http://user-svc:80/signup', json=user_info)
    
    if response.status_code == 200:
        # return jsonify({'message': 'Signup successful', 'data': response.json()}), 200
        return redirect('/pantry')
    else:
        error_message = f"Error: {response.status_code} - {response.reason}"
        return jsonify({'error': 'Signup failed', 'data': response.json()}), response.status_code

@app.route('/pantry')
def pantry():
    # Render your catalog page here
    response = requests.get('http://pantry-svc/pantry')
    if response.status_code == 200:
        items = response.json()
        return render_template('pantry.html', items=items)
    else:
        return jsonify({'error': 'Failed to fetch pantry items'}), response.status_code

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--port', type=int, default=8000, help='Port number')
#     args = parser.parse_args()
#     app.run(debug=True, port=args.port)

# login = input('Do you want to log in (1) or sign up (2)?')
# if login == 1:
#     username = input('Username: ')
#     password = input('Password: ')
#     r = requests.post('http://127.0.0.1:5000/login', json = {'name': username, 'pwd': password})
# else:
#     username = input('Username: ')
#     password = input('Password: ')
#     r = requests.post('http://127.0.0.1:5000/signup', json = {'name': username, 'pwd': password})
# # data = r.json()
# # print(r.json())
# if r.status_code == 200:
#     print("Request successful!")
#     try:
#         print(r.json())
#     except Exception as e:
#         print("Error decoding JSON:", e)
# else:
#     print("Request failed with status code:", r.status_code)
#     print("Response content:", r.text)
# print('Hello'+data['name'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)

