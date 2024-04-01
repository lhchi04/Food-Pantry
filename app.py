from flask import Flask, render_template

app = Flask(__name__)


@app.route('/getName/<name>')
def hello(name):
    return render_template('index.html', username = str(name))

def getName():
    return "Tuan"
