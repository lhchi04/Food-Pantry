import os
import json
import requests
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template


login = input('Do you want to log in (1) or sign up (2)?')
if login == 1:
    username = input('Username: ')
    password = input('Password: ')
    r = requests.post('http://127.0.0.1:5000/login', json = {'name': username, 'pwd': password})
    print(r)
    
    
# @app.route('/', methods=['GET'])
# def hello():
#     r = requests.get('http://name-svc:80') 
#     data = r.json()
#     print(data)
#     return render_template('index.html', username=data['name'])

# if __name__ == '__main__':
#     app.run(debug=True)

