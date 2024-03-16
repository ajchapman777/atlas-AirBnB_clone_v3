from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    """
    Route that returns status
    """
    "status": "OK"
    return
