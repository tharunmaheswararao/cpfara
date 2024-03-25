from flask import Blueprint, render_template, request, jsonify

from backend.services.institute import common_events

institute_frontend_blueprint = Blueprint('institute_frontend', __name__)


############# API ROUTES ----------------> START

def aicte_events(bp):
    @bp.route('/aicte-events', methods=['POST'])
    def aicteevents():
        data = request.get_json()
        response = common_events.aicte_events_renderer(data)
        return response
    
def iit_events(bp):
    @bp.route('/iit-events', methods=['POST'])
    def iitevents():
        data = request.get_json()
        response = common_events.iit_events_renderer(data)
        return response
    
def srm_events(bp):
    @bp.route('/srm-events', methods=['POST'])
    def srmevents():
        data = request.get_json()
        response = common_events.srm_events_renderer(data)
        return response
    
def iiita_events(bp):
    @bp.route('/iiita-events', methods=['POST'])
    def iiitaevents():
        data = request.get_json()
        response = common_events.iiita_events_renderer(data)
        return response

############# API ROUTES ----------------> END

############# FRONTEND ROUTES ----------------> START

@institute_frontend_blueprint.route("/<path:subpath>")
def institute(subpath):
    return render_template("./components/institute.html")

############# FRONTEND ROUTES ----------------> END