#!/usr/bin/python3
""" Module that handles all default RestFul API actions for Users"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrive_users():
    """
    Returns a list of all current users
    """
    users_list = []
    all_users = storage.all(User).values()

    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>/', methods=['GET'],
                 strict_slashes=False)
def retrive_user(user_id):
    """ Returns a User that matches a given id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_user(user_id):
    """
    Deletes a User that matches the given id
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    """
    Creates a new User
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    info = request.get_json()
    user_inst = User(**info)
    user_inst.save()
    return make_response(jsonify(user_inst.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User record
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    titles = ['id', 'created_at', 'updated_at', 'email']
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    info = request.get_json()
    for key, value in info.items():
        if key not in titles:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
