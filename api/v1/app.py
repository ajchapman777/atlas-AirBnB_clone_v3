#!/usr/bin/python3
"""
This module initializes the Flask application
and sets up routes for the API.

It creates a Flask application instance,
registers the blueprint containing API routes,
and configures the application to close the
database connection after each request.
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(self):
    """
    Method that calls close
    """
    storage.close()


host = getenv('HBNB_API_HOST', default='0.0.0.0')
port = getenv('HBNB_API_PORT', default=5000)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
