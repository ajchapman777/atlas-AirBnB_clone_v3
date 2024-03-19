#!/usr/bin/python3
"""
This module contains views for handling
server status and retrieving statistics.

It provides routes to retrieve the status
of the server and statistics about the
stored objects.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_stats():
    """
    Returns the status of the server
    """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """
    Retrieve the number of each object by type
    """

    total_count = storage.count()
    counts_by_type = {}
    for cls in storage.classes():
        counts_by_type[cls.__name__] = storage.count(cls)

    return jsonify({
        'total_count': total_count,
        'counts_by_type': counts_by_type
    })
