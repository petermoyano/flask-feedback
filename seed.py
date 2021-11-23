from app import app

def seed_users():
    """Fills db with some users meant for testing"""
    user1 = User(username="user1")
