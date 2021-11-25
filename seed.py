from app import app
from models import Feedback, User, db

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

def seed_feedbacks():
    """Fills db with some users meant for testing"""
    feedback1 = Feedback(title= "Atta boy!", content= "Ringo is great", username="user1")
    feedback2 = Feedback(title= "You can do better", content= "John is not such a great college", username="user2")
    feedback3 = Feedback(title= "Good job!", content= "Keep up the good work, Paul!", username="user3")

    db.session.add(feedback1)
    db.session.add(feedback2)
    db.session.add(feedback3)

    db.session.commit()
    
seed_feedbacks()