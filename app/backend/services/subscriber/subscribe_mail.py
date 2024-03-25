from flask import jsonify, request
from datetime import datetime
from sqlalchemy import and_

from backend.models.model import Institutions, insert_row, commit_session, rollback_session
from backend.models.database import db

def mail_subscription(user_data):
    try:
        return
    except Exception as e:
        rollback_session()
        return jsonify({"status": False, "error": str(e)})