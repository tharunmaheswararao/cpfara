from flask import jsonify

from backend.models.model import User, insert_row, commit_session, rollback_session
from backend.models.database import db


def insert_user_info(user_data):
    try:
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        
        new_user = User(
            username = username,
            mail_id = email,
            password = password
        )
        insert_row(new_user)
        commit_session()

        response = jsonify({'message': 'User created successfully!'})
        return response
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})
    
def login_verification(user_data):
    try:
        username = user_data['username']
        password = user_data['password']

        user_details = User.query.filter_by(username=username).all()
        print(len(user_details))
        if(len(user_details) == 0):
            return jsonify({"error": "There is no user with that username"})
        elif(len(user_details) > 0 and user_details[0].password == password):
            return jsonify({"message": "success"})
        else:
            return jsonify({"error": "Please provide correct password"})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})