#!/usr/bin/python3
"""
This script starts a Flask web application with three routes.
"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" when accessing the root route.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """
    Display "HBNB" when accessing the /hbnb route.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """
    Display "C " followed by the value of the text variable
    (replace underscore _ symbols with a space)
    """
    text = escape(text.replace('_', ' '))
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
