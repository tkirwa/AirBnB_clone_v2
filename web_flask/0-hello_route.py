#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask


app = Flask(__name__)


# @app.route('/', strict_slashes=False)
# def hello():
#     """
#     Display "Hello HBNB!" when accessing the / route.
#     """
#     return 'Hello HBNB!'


@app.route("/airbnb-onepage/", strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" when accessing the /airbnb-onepage/ route.
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
