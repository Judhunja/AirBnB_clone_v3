#!/usr/bin/python3
""" This module handles all default RESTful API actions
for User objects """
from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    "/cities/<city_id>/places", methods=["GET", "POST"], strict_slashes=False
)
def get_places_objects(city_id):
    """Retrieves the list of all User objects"""
    if request.method == "GET":
        pl = storage.get(City, city_id)
        if pl is None:
            abort(404)
        place = [place.to_dict() for place in pl.places]
        return jsonify(place), 200

    elif request.method == "POST":
        # create new state
        pl = storage.get(City, city_id)
        if pl is None:
            abort(404)
        req = request.get_json()
        if us is None:
            abort(404)
        if not req:
            return jsonify({"error": "Not a JSON"}), 400
        elif "name" not in req:
            return jsonify({"error": "Missing name"}), 400
        elif "user_id" not in req:
            return jsonify({"error": "Missing user_id"}), 400
        us = storage.get(User, req['user_id'])
        new = Place(**req)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
    "/places/<place_id>",
    methods=["GET", "PUT", "DELETE"],
    strict_slashes=False
)
def place_actions(place_id):
    """Performs actions on user objects"""
    if request.method == "GET":
        # retrieve state object
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())

    elif request.method == "DELETE":
        # delete a state
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        place.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        # update state
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400

        for key, val in req.items():
            if key != "id" and key != "user_id"\
                    and key != "city_id"\
                    and key != "created_at"\
                    and key != "updated_at":
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict()), 200
