#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status')
def json_return():
    """ Returns a JSON {"status": "OK"} """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def return_count():
    """ Retrieves the number of each object by type """
    classes = {}
    classes["amenities"] = storage.count("Amenity")
    classes["cities"] = storage.count("City")
    classes["places"] = storage.count("Place")
    classes["reviews"] = storage.count("Review")
    classes["states"] = storage.count("State")
    classes["users"] = storage.count("User")
    return jsonify(classes)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
