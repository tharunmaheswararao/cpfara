from backend.controllers.user import user_frontend_blueprint, \
    user_signup, user_login
from backend.controllers.institute import aicte_events, iit_events, srm_events, iiita_events, institute_frontend_blueprint
from backend.services.institute.common_events import aicte_events_adder, iit_events_adder
from backend.controllers.subscriber import subscriber_frontend_blueprint


from flask import Flask, Blueprint, redirect, render_template, request, url_for
from flask_cors import CORS
from backend.models.database import db
from backend.models import model
import config
import schedule
import threading
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# DATABASE CONFIGURATIONS
db_uri = config.get_db_uri()

# FLASK APP CONFIGURATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

# INITIATE DB OBJECT
db.init_app(app)
with app.app_context():
    model.create_all_tables()

user_api_blueprint = Blueprint('user_api', __name__)
user_signup(user_api_blueprint)
user_login(user_api_blueprint)

institute_api_blueprint = Blueprint('institute_api', __name__)
aicte_events(institute_api_blueprint)
iit_events(institute_api_blueprint)
srm_events(institute_api_blueprint)
iiita_events(institute_api_blueprint)

subscriber_api_blueprint = Blueprint('subscriber_api', __name__)



# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html')

# @app.route("/events")
# def events():
#     return render_template('events.html')

# @app.route("/institute/<path:subpath>")
# def institute(subpath):
#     return render_template('./components/institute.html')

# @app.route("/sih")
# def sih():
#     return render_template('sih.html')

# @app.route("/subscribe")
# def subscribe():
#     return render_template('subscribe.html')

# @app.route("/login")
# def login():
#     return render_template('login.html')

##### SCRAPPER #####

# Define the function to be called
# def my_function():
#     with app.app_context():
        # aicte_events_adder()
        # print("AICTE Scrapper called at", time.strftime("%H:%M:%S"))
        # iit_events_adder()
        # print("IIT Scrapper called at", time.strftime("%H:%M:%S"))

# Schedule the function to be called every 5 seconds
# schedule.every(30).seconds.do(my_function)

# Function to run the scheduler in a separate thread
# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# Start the scheduler thread when the Flask app starts
# scheduler_thread = threading.Thread(target=run_scheduler)
# scheduler_thread.start()

##### SCRAPPER #####

app.register_blueprint(subscriber_api_blueprint, url_prefix='/api/subscriber')
app.register_blueprint(subscriber_frontend_blueprint)

app.register_blueprint(institute_api_blueprint, url_prefix='/api/institute')
app.register_blueprint(institute_frontend_blueprint, url_prefix='/institute')

app.register_blueprint(user_api_blueprint, url_prefix='/api/user')
app.register_blueprint(user_frontend_blueprint)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
