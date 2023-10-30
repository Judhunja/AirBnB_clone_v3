#!/usr/bin/python3
""" This module handles all default RESTful API actions
for User objects """
from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.amenity import Amenity


@app_views.route(
    "/users", methods=["GET", "POST"], strict_slashes=False
)
def get_user_objects():
    """Retrieves the list of all User objects"""
    if request.method == "GET":
        us = storage.all('User')
        if us is None:
            abort(404)
        user = [user.to_dict() for user in us.values()]
        return jsonify(user), 200

    elif request.method == "POST":
        # create new state
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400
        elif "email" not in req:
            return jsonify({"error": "Missing email"}), 400
        elif "password" not in req:
            return jsonify({"error": "Missing email"}), 400
        new = User(**req)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
    "/users/<user_id>",
    methods=["GET", "PUT", "DELETE"],
    strict_slashes=False
)
def user_actions(user_id):
    """Performs actions on user objects"""
    if request.method == "GET":
        # retrieve state object
        user = storage.get('User', user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())

    elif request.method == "DELETE":
        # delete a state
        user = storage.get('User', user_id)
        if user is None:
            abort(404)
        user.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        # update state
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400

        for key, val in req.items():
            if key != "id" and key != "email"\
                    and key != "created_at"\
                    and key != "updated_at":
                setattr(user, key, val)
        user.save()
        return jsonify(user.to_dict()), 200
