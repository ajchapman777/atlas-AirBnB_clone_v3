#!/usr/bin/python3
"""
View for Amenity objects
"""
from flask import jsonify, abort, request
from models import storage, Amenity
from api.v1.views import app_views


def make_request(data, status_code):
    """Helper function to create a response with JSON data and status code."""
    response = jsonify(data)
    response.status_code = status_code
    return response


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    amenities = storage.all(Amenity).values()
    return make_request([amenity.to_dict() for amenity in amenities], 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return make_request(amenity.to_dict(), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_request({}, 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a Amenity."""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_request(amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_request(amenity.to_dict(), 200)

