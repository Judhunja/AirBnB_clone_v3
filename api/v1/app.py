#!/usr/bin/python3
""" Handles 404 errors and closes the app after complete
request """
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def closes(request):
    """ Closes after a request """
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """ Returns a JSON-formatted 404 status reponse code """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", 5000)), threaded=True)
