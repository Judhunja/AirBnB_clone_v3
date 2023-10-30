#!/usr/bin/python3
""" This module handles all default RESTful API actions
for amenity objects """
from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.amenities import Amenity


@app_views.route(
    "/amenities", methods=["GET", "POST"], strict_slashes=False
)
def get_amenity_objects():
    """Retrieves the list of all State objects"""
    if request.method == "GET":
        am = storage.get(Amenity)
        if am is None:
            abort(404)
        amenity = [amen.to_dict() for amen in am.values()]
        return jsonify(amenity), 200

    elif request.method == "POST":
        # create new state
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in req:
            return jsonify({"error": "Missing name"}), 400
        new = Amenity(**req)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
    "/cities/<city_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False
)
def city_actions(city_id):
    """Performs actions on state objects"""
    if request.method == "GET":
        # retrieve state object
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())

    elif request.method == "DELETE":
        # delete a state
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 204

    elif request.method == "PUT":
        # update state
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400

        for key, val in req.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(amenity, key, val)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
