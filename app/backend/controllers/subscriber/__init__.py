from flask import Blueprint, render_template, request, jsonify

from backend.services.subscriber import subscribe_mail

subscriber_frontend_blueprint = Blueprint('subscriber_frontend', __name__)


############# API ROUTES ----------------> START

def subscriber_mail(bp):
    @bp.route('/subscribe' , methods=['POST'])
    def mail():
        data = request.get_json()
        response = subscribe_mail.mail_subscription(data)
        return response

############# API ROUTES ----------------> END

############# FRONTEND ROUTES ----------------> START

@subscriber_frontend_blueprint.route("/subscribe")
def subscribe():
    return render_template("./subscribe.html")

############# FRONTEND ROUTES ----------------> END