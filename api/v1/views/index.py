#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def json_return():
    """ Returns a JSON {"status": "OK"} """
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
