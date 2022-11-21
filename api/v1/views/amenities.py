#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrives_amenities():
    """
    Returns a list of all available amenities
    """
    amenities_list = []
    allamenities = storage.all(Amenity).values()

    for amenity in allamenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def retrive_amenity(amenity_id):
    """ Returns an amenity of a given id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_amenity(amenity_id):
    """
    Removes an amenity of an  Object
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new amenity using the POST method
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    info = request.get_json()
    amenity_inst = Amenity(**info)
    amenity_inst.save()
    return make_response(jsonify(amenity_inst.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    PUT method used to update amenity info
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    titles = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    info = request.get_json()
    for key, value in info.items():
        if key not in titles:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
