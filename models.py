from enum import unique
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def connect_db(app):
    """From within app.py we import this function to connect our Flask app to our db"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__="users"
    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text(50), unique=True, nullable=False)
    first_name = db.Column(db.Text(30), nullable=False)
    first_name = db.Column(db.Text(30), nullable=False)

