from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash
from sqlalchemy.orm import backref



db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """From within app.py we import this function to connect our Flask app to our db"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Represents the table users with their login information"""
    __tablename__="users"
    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback', backref='user', cascade="all,delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password & return user"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate credentials for login, return user if correct, else False"""
        current_user = User.query.filter_by(username=username).first()
        if current_user and bcrypt.check_password_hash(current_user.password, password):
            return current_user
        else:
            return False
#    @classmethod
#    def delete(cls, username):
#        """Delete the user from the db"""
#        current_user = User.query.filter_by(username=username).delete()
#        db.session.commit()

class Feedback(db.Model):
    """Feedbacks table with source information"""
    __tablename__="feedbacks"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username')) 



        