#!/usr/bin/python3
"""
View for Cities
"""

from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


# Retrieve all cities of a state
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    if state_object is None:
        abort(404)
        response = request.get_json(silent=True)
        if not response:
            return make_response(jsonify({'error': 'Not a JSON'}))


# Retrieve a specific city
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


# Delete a city
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


# Create a new city
@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


# Update a city
@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
