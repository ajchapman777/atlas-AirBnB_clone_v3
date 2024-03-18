from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, State, City

@app_views.route('/states/<state_id>/cities', 
