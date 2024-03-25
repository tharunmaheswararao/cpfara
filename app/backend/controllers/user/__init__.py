from flask import Blueprint, render_template, request, jsonify

from backend.services.user import signin

user_frontend_blueprint = Blueprint('user_frontend', __name__)

############# API ROUTES ----------------> START

def user_signup(bp):
    @bp.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        response = signin.insert_user_info(data)
        return response
    
def user_login(bp):
    @bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        response = signin.login_verification(data)
        return response
    

############# API ROUTES ----------------> END

############# FRONTEND ROUTES ----------------> START
    
@user_frontend_blueprint.route("/signup")
def signup():
    return render_template('signup.html')

@user_frontend_blueprint.route("/login")
@user_frontend_blueprint.route("/")
def login():
    return render_template('login.html')

@user_frontend_blueprint.route("/home")
def home():
    return render_template('home.html')

############# FRONTEND ROUTES ----------------> END