# Flask version 1.0.2
# Python version 3.6.4
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
