#!/usr/bin/python3
""" This module handles all default RESTful API actions
for city objects """
from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.state import State
from models.city import City


@app_views.route(
    "/states/<state_id>/cities", methods=["GET", "POST"], strict_slashes=False
)
def get_city_objects(state_id):
    """Retrieves the list of all State objects"""
    if request.method == "GET":
        st = storage.get(State, state_id)
        if st is None:
            abort(404)
        cities = [city.to_dict() for city in st.cities]
        return jsonify(state), 200

    elif request.method == "POST":
        # create new state
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in req:
            return jsonify({"error": "Missing name"}), 400
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        req["state_id"] = state_id
        new = City(**req)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
    "/cities/<city_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False
)
def city_actions(city_id):
    """Performs actions on state objects"""
    if request.method == "GET":
        # retrieve state object
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        # delete a state
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        city.delete()
        storage.save()
        return jsonify({}), 204

    elif request.method == "PUT":
        # update state
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400

        for key, val in req.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict()), 200
