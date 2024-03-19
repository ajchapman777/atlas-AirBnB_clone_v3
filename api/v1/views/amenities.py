#!/usr/bin/python3
"""Defines API routes for Amenity objects."""

from flask import jsonify, abort, request
from models import storage, Amenity
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Retrieves the list of all Amenity objects."""
    amenities = [
        amenity.to_dict()
        for amenity in storage.all(Amenity).values()
    ]
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a Amenity."""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
