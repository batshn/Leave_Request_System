# type "python3 flask_init.py" in terminal to start app
from flask import Flask
import os, requests
from flask_base import base
import webbrowser
from threading import Timer

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.register_blueprint(base)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=5000, debug=True)
