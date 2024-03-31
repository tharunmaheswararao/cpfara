from backend.models.database import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extended_existing' : True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    mail_id = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Events(db.Model):
    __tablename__ = 'events'
    __table_args__ = {'extended_existing' : True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_date = db.Column(db.Date)
    event_description = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    event_type = db.Column(db.String(255), nullable=False)


class Institutions(db.Model):
    __tablename__ = 'institutions'
    __table_args__ = {'extended_existing' : True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_date = db.Column(db.Date, nullable=True)
    event_description = db.Column(db.String(500), nullable=False)
    domain = db.Column(db.String(255), nullable=True)
    college_name = db.Column(db.String(255), nullable=True)


class Subscribe(db.Model):
    __tablename__ = 'Subscribe'
    __table_args__ = {'extended_existing' : True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    mail_id = db.Column(db.String(255), unique=True, nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date)
    college_name = db.Column(db.String(255), nullable=False)
    event_description = db.Column(db.String(255), nullable=False)



##### HELPER METHODS ######
def create_all_tables():
    db.create_all()

def insert_row(row):
    db.session.add(row)
    db.session.flush()


def insert_multiple_row(rows):
    db.session.add_all(rows)
    db.session.flush()


def commit_session():
    db.session.commit()


def rollback_session():
    db.session.rollback()
    db.session.commit()


def delete_row(rows):
    db.session.delete(rows)
    db.session.flush()
