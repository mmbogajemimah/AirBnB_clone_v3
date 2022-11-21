#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrive_cities(state_id):
    """
    Gets back a list of specific cities
    """
    cities_list = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def retrive_city(city_id):
    """
    Gives back a specific city based on id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def remove_city(city_id):
    """
    Removes permanently a city based on id provided
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    info = request.get_json()
    city_inst = City(**info)
    city_inst.state_id = state.id
    city_inst.save()
    return make_response(jsonify(city_inst.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City using PUT method
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    titles = ['id', 'state_id', 'created_at', 'updated_at']

    info = request.get_json()
    for key, value in data.info():
        if key not in titles:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
