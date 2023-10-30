#!/usr/bin/python3
""" This module handles all default RESTful API actions
for State objects """
from api.v1.views import app_views
from models import storage
from flask import request, jsonify


@app_views.route("/states")
def get_objects():
    """Retrieves the list of all State objects"""
    st = storage.all("State")
    state = [state.to_dict() for state in st.values]
    return jsonify(state)


@app_views.route("/states/<state_id>",
                 methods=["GET", "POST", "PUT", "DELETE"])
def get_state(id):
    """Retrieves a state object"""
    if request.method == "GET":
        # retrieve state object
        state = storage.get(State, id)
        if state is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(state.to_dict())

    elif request.method == "POST":
        # create new state
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in req:
            return jsonify({"Missing name"}), 400
        new = State(**req)
        new.save()
        return jsonify(new.to_dict()), 201

    elif request.method == "PUT":
        # update state
        state = storage.get(State, id)
        if state is None:
            return jsonify({"error": "Not found"}), 404
        req = request.get_json()
        if not req:
            return jsonify({"error": "Not a JSON"}), 400
        for key, val in req.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(state, key, val)
        state.save()
        return jsonify(state.to_dict()), 200

    elif request.method == "DELETE":
        # delete a state
        state = storage.get(State, state_id)
        if state is None:
            return jsonify({"error": "Not found"}), 404
        state.delete()
        return jsonify({}), 204
