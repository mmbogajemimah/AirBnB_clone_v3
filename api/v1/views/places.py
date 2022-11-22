#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Places """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrive_places(city_id):
    """
    Returns a list of places in a city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrive_place(place_id):
    """
    Returns a Place object in a city
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_place(place_id):
    """
    Removes info of a Place Object in a city with specific id
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place in a city with a specific id
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    info = request.get_json()
    user = storage.get(User, info['user_id'])

    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    info["city_id"] = city_id
    place_inst = Place(**info)
    place_inst.save()
    return make_response(jsonify(place_inst.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place using the PUT method
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    info = request.get_json()
    if not info:
        abort(400, description="Not a JSON")

    titles = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in info.items():
        if key not in titles:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects in JSON body request
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    info = request.get_json()

    if info and len(info):
        states = info.get('states', None)
        cities = info.get('cities', None)
        amenities = info.get('amenities', None)

    if not info or not len(info) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        places_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)

    places_list = []
    if states:
        states_object = [storage.get(State, s_id) for s_id in states]
        for state in states_object:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places_list.append(place)

    if cities:
        city_object = [storage.get(City, c_id) for c_id in cities]
        for city in city_object:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_object = [storage.get(Amenity, a_id) for a_id in amenities]
        places_list = [place for place in places_list
                       if all([am in place.amenities
                               for am in amenities_object])]

    places = []
    for pl in places_list:
        data = pl.to_dict()
        data.pop('amenities', None)
        places.append(data)

    return jsonify(places)
