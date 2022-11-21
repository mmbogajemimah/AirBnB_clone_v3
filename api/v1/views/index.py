#!/usr/bin/python3

"""
This module contains some utility functions for the API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """
    Returns Status OK code.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    numberof_objects = {}
    for i in range(len(classes)):
        numberof_objects[names[i]] = storage.count(classes[i])

    return jsonify(numberof_objects)
