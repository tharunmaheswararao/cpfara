from flask import Blueprint, render_template, request, jsonify

from backend.services.events import events

events_frontend_blueprint = Blueprint('events_frontend', __name__)


############# API ROUTES ----------------> START

def kr_events(bp):
    @bp.route('/kr-events', methods=['POST'])
    def krevents():
        data = request.get_json()
        response = events.kr_events_renderer(data)
        return response
    
############# API ROUTES ----------------> END

############# FRONTEND ROUTES ----------------> START
    
@events_frontend_blueprint.route("/events")
def kr_frontend_events():
    return render_template('events.html')

############# FRONTEND ROUTES ----------------> END
