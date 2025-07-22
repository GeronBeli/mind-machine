from models import User
from repositories import UserRepository
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def init_user(self, user_id, is_admin=False):
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if user:
            raise ValueError("User already exists")
        new_user = User(user_id=user_id, is_admin=is_admin)
        self.db.add(new_user)
        self.db.commit()

    def get_user(self, user_id):
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        return user

    def list_users(self):
        return self.db.query(User).all()

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        self.db.delete(user)

    def update_last_login(self, user_id):
        user = self.get_user(user_id)
        user.last_login = datetime.now(timezone.utc)
        self.db.commit()

    def get_active_inactive_counts(self):
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        return {
            "active_users": self.db.query(User).filter(User.last_login > thirty_days_ago).count(),
            "inactive_users": self.db.query(User).filter(User.last_login < thirty_days_ago).count()
        }
