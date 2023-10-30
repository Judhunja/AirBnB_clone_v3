#!/usr/bin/python3
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def closes(request):
    """ Closes after a request """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", 5000)), threaded=True)
