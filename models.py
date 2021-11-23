from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def connect_db(app):
    """From within app.py we import this function to connect our Flask app to our db"""
    db.app = app
    db.init_app(app)
