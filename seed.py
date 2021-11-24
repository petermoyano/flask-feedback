from app import app
from models import User, db

db.drop_all()
db.create_all()

def seed_users():
    """Fills db with some users meant for testing"""
    user1 = User.register(username="user1", password="user1", email="user1@gmail.com", first_name="John", last_name="Lennon")
    user2 = User.register(username="user2", password="user2", email="user2@gmail.com", first_name="Paul", last_name="Brennan")
    user3 = User.register(username="user3", password="user3", email="user3@gmail.com", first_name="Ringo", last_name="Smith")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()
    
seed_users()