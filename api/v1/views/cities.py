#!/usr/bin/python3
"""
This module creates the view for all city objects
and handles all default API actions
"""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """
    This method retrieves a list of all cities in one state
    Args:
        state_id: The ID of the state
    Returns:
        JSON response containing a list of dictionaries with cities
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = [city.to_dict() for city in cities]
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    This method retrieves one city object by its ID
    Args:
        city_id: The ID of the city
    Returns:
        JSON response containing the city object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    This method deletes a city object by its ID
    Args:
        city_id: The ID of the city
    Returns:
        Empty dictionary
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    This method creates a new city object in a given state
    Args:
        state_id: The ID of the state
    Returns:
        JSON response containing the created city object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")

    json_data["state_id"] = state_id
    city = City(**json_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    This method updates a city object by its ID
    Args:
        city_id: The ID of the city
    Returns:
        JSON response containing the updated city object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")

    for key, value in json_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
