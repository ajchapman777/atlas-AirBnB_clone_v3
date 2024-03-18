#!/usr/bin/python3
"""Module to handle City objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, State, City

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object by its id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

if __name__ == "__main__":
    pass  # If you need to add additional functionality, you can do it here
