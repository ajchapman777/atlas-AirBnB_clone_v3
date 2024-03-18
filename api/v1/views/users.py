#!/usr/bin/python3
"""Defines API routes for User objects."""
from flask import jsonify, abort, request
from models import storage, User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects."""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object by its ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        JSON: A JSON representation of the user object.

    Raises:
        404: If no user with the given ID is found.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object by its ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        JSON: An empty dictionary.

    Raises:
        404: If no user with the given ID is found.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new User object.

    Returns:
        JSON: A JSON representation of the newly created user object.

    Raises:
        400: If the request body is not a valid JSON or if required fields are missing.
    """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'email' not in request.json:
        abort(400, description="Missing email")
    if 'password' not in request.json:
        abort(400, description="Missing password")
    data = request.get_json()
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object by its ID.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        JSON: A JSON representation of the updated user object.

    Raises:
        404: If no user with the given ID is found.
        400: If the request body is not a valid JSON.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
