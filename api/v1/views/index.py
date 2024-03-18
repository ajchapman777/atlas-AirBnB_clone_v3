#!/usr/bin/python3
"""Module to handle index routes
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the server
    """
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass  # If you need to add additional functionality, you can do it here


from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    """
    Route that returns status
    """
    "status": "OK"
    return
