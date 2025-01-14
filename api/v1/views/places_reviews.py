#!/usr/bin/python3
"""Module that handles all default RESTful API actions for Reviews"""
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """
    Returns all reviews for the place that matches the ID.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Returns the Review that matches the given ID.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes the Review that matches the given ID
    """

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review for the place that matches the ID.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates the Review that matches the given id.
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    info = request.get_json()
    if not info:
        abort(400, description="Not a JSON")

    titles = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in info.items():
        if key not in titles:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
