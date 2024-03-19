#!/usr/bin/python3
"""
API using Flask
"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(self):
    """
    Method that calls close
    """
    storage.close()
    

host = getenv('HBNB_API_HOST', default='0.0.0.0')
port = getenv('HBNB_API_PORT', default=5000)
   
if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)